"""Handler for the /help command."""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database import db
from utils.i18n import get_text

logger = logging.getLogger(__name__)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command to display instructions and available commands."""
    user = update.effective_user
    if not user:
        return

    lang = await db.get_user_language(user.id)
    help_text = get_text("help", lang=lang)

    keyboard = [
        [
            InlineKeyboardButton("⚙️ Settings", callback_data="nav_settings"),
            InlineKeyboardButton("ℹ️ About", callback_data="nav_about"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            help_text,
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )
    elif update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            help_text,
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )
