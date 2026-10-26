"""Administrator commands and management interface."""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from config import config
from database import db
from services.ai_service import ai_service
from utils.i18n import get_text

logger = logging.getLogger(__name__)


def require_admin(func):
    """Decorator to enforce administrator permissions."""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.effective_user
        if not user or not config.is_admin(user.id):
            logger.warning(
                "Unauthorized admin attempt by user %s (ID: %s)",
                user.username if user else "Unknown",
                user.id if user else "Unknown",
            )
            lang = await db.get_user_language(user.id) if user else "en"
            if update.message:
                await update.message.reply_text(get_text("admin_only", lang=lang))
            return
        return await func(update, context, *args, **kwargs)

    return wrapper


@require_admin
async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /admin command to show admin help and status."""
    if not update.message:
        return

    admin_panel_text = (
        "🛡️ **Telegram Assistant Bot - Admin Panel**\n\n"
        "Welcome, Administrator! Here are your available commands:\n\n"
        "• `/stats` — View system analytics, user counts, and database health.\n"
        "• `/broadcast <message>` — Send an announcement to all registered users.\n\n"
        "⚠️ *Use broadcasts responsibly to avoid user complaints.*"
    )
    await update.message.reply_text(admin_panel_text, parse_mode="Markdown")


@require_admin
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /stats command to report real-time system metrics."""
    user = update.effective_user
    if not user or not update.message:
        return

    lang = await db.get_user_language(user.id)
    stats = await db.get_stats()
    ai_mode = ai_service.get_status_description()

    report = get_text(
        "admin_stats",
        lang=lang,
        total_users=stats["total_users"],
        active_users=stats["active_users"],
        total_messages=stats["total_messages"],
        ai_mode=ai_mode,
        admin_count=len(config.admin_ids),
    )
    await update.message.reply_text(report, parse_mode="Markdown")


@require_admin
async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Broadcast an announcement message to all registered bot users."""
    user = update.effective_user
    if not user or not update.message:
        return

    lang = await db.get_user_language(user.id)
    message_to_send = " ".join(context.args).strip() if context.args else ""

    if not message_to_send:
        await update.message.reply_text(get_text("broadcast_empty", lang=lang), parse_mode="Markdown")
        return

    all_users = await db.get_all_user_ids()
    start_msg = get_text("broadcast_started", lang=lang, total_users=len(all_users))
    status_msg = await update.message.reply_text(start_msg)

    success_count = 0
    fail_count = 0

    for target_user_id in all_users:
        try:
            await context.bot.send_message(
                chat_id=target_user_id,
                text=message_to_send,
                parse_mode="Markdown",
            )
            success_count += 1
        except Exception as e:
            logger.debug("Failed broadcast to user %d: %s", target_user_id, e)
            fail_count += 1

    summary = get_text(
        "broadcast_finished",
        lang=lang,
        success=success_count,
        failed=fail_count,
    )
    await status_msg.edit_text(summary)
