"""Handlers registration module for Telegram Bot Assistant."""

import logging
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from handlers.start import start_command
from handlers.help import help_command
from handlers.about import about_command
from handlers.settings import settings_command, clear_command, settings_callback_handler
from handlers.chat import ask_command, message_handler
from handlers.admin import admin_command, stats_command, broadcast_command

logger = logging.getLogger(__name__)


def register_handlers(app: Application) -> None:
    """Register all command, message, and callback handlers into the application."""
    # Standard user commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("settings", settings_command))
    app.add_handler(CommandHandler("clear", clear_command))
    app.add_handler(CommandHandler("ask", ask_command))

    # Administrator commands
    app.add_handler(CommandHandler("admin", admin_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("broadcast", broadcast_command))

    # Interactive inline keyboard button callbacks
    app.add_handler(CallbackQueryHandler(settings_callback_handler))

    # General conversation message handler (non-command text in private chats)
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)
    )

    logger.info("All bot handlers registered successfully.")
