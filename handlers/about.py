"""Handler for the /about command."""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database import db
from services.ai_service import ai_service
from utils.i18n import get_text

logger = logging.getLogger(__name__)


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /about command to display bot specifications and capabilities."""
    user = update.effective_user
    if not user:
        return

    lang = await db.get_user_language(user.id)
    ai_status = ai_service.get_status_description()

    about_text = get_text("about", lang=lang, ai_engine=ai_status)

    keyboard = [
        [
            InlineKeyboardButton("🔙 Back to Start", callback_data="nav_start"),
            InlineKeyboardButton("📖 Help", callback_data="nav_help"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            about_text,
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )
    elif update.callback_query:
        await update.callback_query.answer()
        try:
            await update.callback_query.edit_message_text(
                about_text,
                reply_markup=reply_markup,
                parse_mode="Markdown",
            )
        except Exception as e:
            if "Message is not modified" not in str(e):
                logger.warning("Failed to edit message in about: %s", e)
