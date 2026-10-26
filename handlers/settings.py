"""Handler for /settings and /clear commands, along with interactive inline callbacks."""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database import db
from utils.i18n import get_text, SUPPORTED_LANGUAGES

logger = logging.getLogger(__name__)


def build_settings_keyboard(current_lang: str) -> InlineKeyboardMarkup:
    """Build the settings inline keyboard."""
    en_label = "✅ English 🇬🇧" if current_lang == "en" else "English 🇬🇧"
    km_label = "✅ ភាសាខ្មែរ 🇰🇭" if current_lang == "km" else "ភាសាខ្មែរ 🇰🇭"

    keyboard = [
        [
            InlineKeyboardButton(en_label, callback_data="set_lang_en"),
            InlineKeyboardButton(km_label, callback_data="set_lang_km"),
        ],
        [
            InlineKeyboardButton("🧹 Clear Conversation Memory", callback_data="clear_memory"),
        ],
        [
            InlineKeyboardButton("🔙 Back to Start", callback_data="nav_start"),
            InlineKeyboardButton("❌ Close", callback_data="close_menu"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the user settings menu."""
    user = update.effective_user
    if not user:
        return

    lang = await db.get_user_language(user.id)
    history_count = await db.get_user_history_count(user.id)
    current_lang_name = SUPPORTED_LANGUAGES.get(lang, "English")

    text = get_text(
        "settings_menu",
        lang=lang,
        current_lang=current_lang_name,
        history_count=history_count,
    )
    reply_markup = build_settings_keyboard(lang)

    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.answer()
        try:
            await update.callback_query.edit_message_text(
                text, reply_markup=reply_markup, parse_mode="Markdown"
            )
        except Exception as e:
            if "Message is not modified" not in str(e):
                logger.warning("Failed to edit message in settings: %s", e)


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /clear command to wipe user conversation history."""
    user = update.effective_user
    if not user:
        return

    await db.clear_conversation_history(user.id)
    lang = await db.get_user_language(user.id)
    reply_text = get_text("memory_cleared", lang=lang)

    if update.message:
        await update.message.reply_text(reply_text, parse_mode="Markdown")


async def settings_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle all button clicks inside settings and navigation menus."""
    query = update.callback_query
    if not query or not query.data or not query.from_user:
        return

    user_id = query.from_user.id
    data = query.data

    if data == "close_menu":
        await query.answer()
        await query.delete_message()
        return

    if data == "clear_memory":
        await db.clear_conversation_history(user_id)
        lang = await db.get_user_language(user_id)
        alert_text = get_text("memory_cleared", lang=lang)
        await query.answer(alert_text, show_alert=True)
        # Refresh the settings menu display
        await settings_command(update, context)
        return

    if data == "set_lang_en":
        await db.set_user_language(user_id, "en")
        alert_text = get_text("language_changed", lang="en")
        await query.answer(alert_text, show_alert=False)
        await settings_command(update, context)
        return

    if data == "set_lang_km":
        await db.set_user_language(user_id, "km")
        alert_text = get_text("language_changed", lang="km")
        await query.answer(alert_text, show_alert=False)
        await settings_command(update, context)
        return

    if data == "nav_toggle_lang":
        current_lang = await db.get_user_language(user_id)
        new_lang = "km" if current_lang == "en" else "en"
        await db.set_user_language(user_id, new_lang)
        alert_text = get_text("language_changed", lang=new_lang)
        await query.answer(alert_text, show_alert=False)
        from handlers.start import start_command
        await start_command(update, context)
        return

    if data == "nav_start":
        from handlers.start import start_command
        await start_command(update, context)
        return

    if data == "nav_help":
        from handlers.help import help_command
        await help_command(update, context)
        return

    if data == "nav_about":
        from handlers.about import about_command
        await about_command(update, context)
        return

    if data == "nav_settings":
        await settings_command(update, context)
        return
