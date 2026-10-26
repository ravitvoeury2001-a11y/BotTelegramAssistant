"""Tests for handler registration with python-telegram-bot Application."""

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
)
from handlers import register_handlers


def test_handlers_registered_correctly():
    """Verify that all commands and callback handlers are properly registered."""
    app = (
        ApplicationBuilder()
        .token("123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ")
        .build()
    )

    register_handlers(app)

    # Handlers are registered under group 0 by default
    group_0 = app.handlers.get(0, [])
    assert len(group_0) > 0

    command_handlers = [h for h in group_0 if isinstance(h, CommandHandler)]
    callback_handlers = [h for h in group_0 if isinstance(h, CallbackQueryHandler)]
    message_handlers = [h for h in group_0 if isinstance(h, MessageHandler)]

    # Extract all command strings
    registered_commands = set()
    for h in command_handlers:
        registered_commands.update(h.commands)

    expected_commands = {
        "start",
        "help",
        "about",
        "settings",
        "clear",
        "ask",
        "admin",
        "stats",
        "broadcast",
    }

    assert expected_commands.issubset(registered_commands)
    assert len(callback_handlers) >= 1
    assert len(message_handlers) >= 1
