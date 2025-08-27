"""Handlers for displaying moderation logs and reputation."""

from aiogram import Router, F
from aiogram.types import Message

from sentinelmod.handlers.middleware.role_check import RoleCheckMiddleware
from sentinelmod.services import moderation as moderation_service


router = Router()
router.message.middleware(RoleCheckMiddleware("moderator"))


@router.message(F.text.startswith("!logs"))
async def cmd_logs(msg: Message) -> None:
    """Show full moderation log for a user."""
    if not msg.reply_to_message:
        await msg.reply("Используйте в ответ на сообщение")
        return
    target = msg.reply_to_message.from_user
    logs = await moderation_service.get_logs(msg.chat.id, target.id)
    if not logs:
        await msg.reply("Нет записей")
        return
    lines = [
        f"{entry.created_at:%Y-%m-%d %H:%M} {entry.action}: {entry.reason or ''}"
        for entry in logs
    ]
    await msg.reply("\n".join(lines))


@router.message(F.text.startswith("!rep"))
async def cmd_rep(msg: Message) -> None:
    """Show public moderation records for a user."""
    target = msg.reply_to_message.from_user if msg.reply_to_message else msg.from_user
    logs = await moderation_service.get_logs(
        msg.chat.id, target.id, public_only=True
    )
    if not logs:
        await msg.reply("Нет записей")
        return
    lines = [
        f"{entry.created_at:%Y-%m-%d %H:%M} {entry.action}: {entry.reason or ''}"
        for entry in logs
    ]
    await msg.reply("\n".join(lines))

