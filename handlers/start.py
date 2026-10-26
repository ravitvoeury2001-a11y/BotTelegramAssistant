"""Handler for the /start command."""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database import db
from utils.i18n import get_text

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command, register user, and present welcome interface."""
    user = update.effective_user
    if not user:
        return

    # Upsert user record
    await db.upsert_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
    )

    # Get user language
    lang = await db.get_user_language(user.id)
    first_name = user.first_name or "Friend"

    welcome_text = get_text("welcome", lang=lang, name=first_name)

    # Interactive Inline Keyboard for quick navigation
    keyboard = [
        [
            InlineKeyboardButton("📖 Help", callback_data="nav_help"),
            InlineKeyboardButton("⚙️ Settings", callback_data="nav_settings"),
        ],
        [
            InlineKeyboardButton("ℹ️ About", callback_data="nav_about"),
            InlineKeyboardButton("🌐 ភាសាខ្មែរ / English", callback_data="nav_toggle_lang"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )
    elif update.callback_query:
        await update.callback_query.answer()
        try:
            await update.callback_query.edit_message_text(
                welcome_text,
                reply_markup=reply_markup,
                parse_mode="Markdown",
            )
        except Exception as e:
            if "Message is not modified" not in str(e):
                logger.warning("Failed to edit message in start: %s", e)
