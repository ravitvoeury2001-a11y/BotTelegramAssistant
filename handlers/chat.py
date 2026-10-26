"""Handler for user conversation and /ask command with memory and rate limiting."""

import logging
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from config import config
from database import db
from services.ai_service import ai_service
from utils.i18n import get_text
from utils.rate_limiter import RateLimiter

logger = logging.getLogger(__name__)

# Initialize rate limiter with configured cooldown seconds
rate_limiter = RateLimiter(cooldown_seconds=config.rate_limit_seconds)


async def send_typing_indicator(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send typing action to indicate the bot is processing."""
    try:
        if update.effective_chat:
            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id,
                action=ChatAction.TYPING,
            )
    except Exception as e:
        logger.debug("Failed to send typing indicator: %s", e)


async def send_safe_message(update: Update, text: str) -> None:
    """Send response safely handling Telegram's 4096 char limit and Markdown parse errors."""
    if not update.message or not text:
        return

    # Telegram message length limit is 4096
    max_len = 4000
    chunks = [text[i : i + max_len] for i in range(0, len(text), max_len)]

    for chunk in chunks:
        try:
            await update.message.reply_text(chunk, parse_mode="Markdown")
        except Exception:
            # Fallback to plain text if Markdown parsing fails
            await update.message.reply_text(chunk)


async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /ask <question> command."""
    user = update.effective_user
    if not user or not update.message:
        return

    # Ensure user is recorded
    await db.upsert_user(user.id, user.username, user.first_name)
    lang = await db.get_user_language(user.id)

    # Extract query after /ask
    prompt = " ".join(context.args).strip() if context.args else ""
    if not prompt:
        empty_msg = get_text("ask_empty", lang=lang)
        await update.message.reply_text(empty_msg, parse_mode="Markdown")
        return

    await process_chat_message(update, context, prompt, user.id, lang)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming regular text messages in private chats as conversation."""
    user = update.effective_user
    if not user or not update.message or not update.message.text:
        return

    prompt = update.message.text.strip()
    # Ignore commands (starting with '/')
    if prompt.startswith("/"):
        return

    # Ensure user is recorded
    await db.upsert_user(user.id, user.username, user.first_name)
    lang = await db.get_user_language(user.id)

    await process_chat_message(update, context, prompt, user.id, lang)


async def process_chat_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    prompt: str,
    user_id: int,
    lang: str,
) -> None:
    """Process user message through rate limiter, memory lookup, and AI service."""
    # 1. Check Rate Limiter
    allowed, wait_seconds = rate_limiter.is_allowed(user_id)
    if not allowed:
        limit_msg = get_text("rate_limited", lang=lang, seconds=wait_seconds)
        if update.message:
            await update.message.reply_text(limit_msg)
        return

    # 2. Show Typing Indicator
    await send_typing_indicator(update, context)

    # 3. Fetch Recent Conversation History for Context Memory
    history = await db.get_conversation_history(
        user_id=user_id, limit=config.max_memory_messages
    )

    # 4. Generate AI response
    try:
        response_text = await ai_service.generate_response(
            prompt=prompt,
            conversation_history=history,
            language=lang,
        )
    except Exception as e:
        logger.error("Error generating AI response for user %d: %s", user_id, e)
        response_text = get_text("error_generic", lang=lang)

    # 5. Persist interaction into database
    await db.save_message(user_id=user_id, role="user", content=prompt)
    await db.save_message(user_id=user_id, role="assistant", content=response_text)

    # 6. Deliver response
    await send_safe_message(update, response_text)
