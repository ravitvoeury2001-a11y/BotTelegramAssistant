"""Main entry point for the Telegram Bot Assistant."""

import logging
import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, Application, ContextTypes

from config import config
from database import db
from handlers import register_handlers
from services.ai_service import ai_service
from utils.logging_config import setup_logging
from utils.i18n import get_text

# Initialize logger
logger = setup_logging(config.log_level)


async def post_init(application: Application) -> None:
    """Async hook called once when the bot application starts up."""
    # Initialize SQLite database tables
    await db.init_db()

    # Fetch bot metadata
    bot_info = await application.bot.get_me()
    logger.info("=" * 60)
    logger.info("🤖 TELEGRAM BOT ASSISTANT STARTED SUCCESSFULLY")
    logger.info("• Bot Name:       %s", bot_info.first_name)
    logger.info("• Username:       @%s", bot_info.username)
    logger.info("• Bot ID:         %s", bot_info.id)
    logger.info("• AI Backend:     %s", ai_service.get_status_description())
    logger.info("• Admins:         %s", config.admin_ids or "None configured")
    logger.info("• Database Path:  %s", config.database_path)
    logger.info("=" * 60)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Global error handler for all unhandled exceptions.

    Logs error details internally without exposing sensitive details, API keys,
    or internal tracebacks to the end-user.
    """
    logger.error("Exception while handling an update:", exc_info=context.error)

    # Inform the user politely if this error happened inside an active conversation
    if isinstance(update, Update) and update.effective_message:
        try:
            user_id = update.effective_user.id if update.effective_user else 0
            lang = await db.get_user_language(user_id) if user_id else "en"
            friendly_error = get_text("error_generic", lang=lang)
            await update.effective_message.reply_text(friendly_error)
        except Exception as e:
            logger.error("Failed to notify user about error: %s", e)


# Ensure UTF-8 output on Windows consoles if supported
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def print_startup_banner() -> None:
    """Print an aesthetic ASCII banner and status summary to the console."""
    banner = """
==========================================================================
                 TELEGRAM BOT ASSISTANT (PYTHON 3.12+)
                      Intelligent Conversational AI
==========================================================================
"""
    print(banner)


def main() -> None:
    """Run the bot polling loop."""
    print_startup_banner()

    # Validate essential configuration
    config_errors = config.validate()
    if config_errors:
        print("\n❌ CONFIGURATION ERROR:")
        for err in config_errors:
            print(f"  • {err}")
        print("\n👉 Please configure your .env file. See .env.example for instructions.")
        print("   On Windows Command Prompt:  copy .env.example .env")
        print("   On PowerShell:             cp .env.example .env\n")
        sys.exit(1)

    try:
        # Build Telegram Application
        application = (
            ApplicationBuilder()
            .token(config.telegram_bot_token)
            .post_init(post_init)
            .build()
        )

        # Register command and message handlers
        register_handlers(application)

        # Register centralized error handler
        application.add_error_handler(error_handler)

        logger.info("Starting polling loop... Press Ctrl+C to stop.")
        application.run_polling(drop_pending_updates=True)

    except KeyboardInterrupt:
        logger.info("Bot stopped by user (Ctrl+C). Goodbye!")
    except Exception as e:
        logger.critical("Fatal error starting bot: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
