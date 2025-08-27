from aiogram import Router, F
from aiogram.types import Message

from sentinelmod.services import moderation as moderation_service
from sentinelmod.handlers.middleware.role_check import RoleCheckMiddleware

router = Router()
router.message.middleware(RoleCheckMiddleware("moderator"))


@router.message(F.text.startswith("!warn"))
async def cmd_warn(msg: Message) -> None:
    if not msg.reply_to_message:
        await msg.reply("Используйте в ответ на сообщение")
        return
    reason = msg.text.partition(" ")[2] or "Без причины"
    await moderation_service.warn_user(msg, msg.reply_to_message.from_user, reason)


@router.message(F.text.startswith("!ban"))
async def cmd_ban(msg: Message) -> None:
    if not msg.reply_to_message:
        await msg.reply("Используйте в ответ на сообщение")
        return
    args = msg.text.partition(" ")[2]
    duration, reason = moderation_service.parse_time_and_reason(args)
    await moderation_service.ban_user(
        msg, msg.reply_to_message.from_user, duration, reason
    )


@router.message(F.text.startswith("!mute"))
async def cmd_mute(msg: Message) -> None:
    if not msg.reply_to_message:
        await msg.reply("Используйте в ответ на сообщение")
        return
    args = msg.text.partition(" ")[2]
    duration, reason = moderation_service.parse_time_and_reason(args)
    if duration is None:
        await msg.reply("Укажите длительность")
        return
    await moderation_service.mute_user(
        msg, msg.reply_to_message.from_user, duration, reason
    )


@router.message(F.text.startswith("!ro"))
async def cmd_ro(msg: Message) -> None:
    # read-only is implemented as mute
    await cmd_mute(msg)


@router.message(F.text.startswith("!unmute"))
async def cmd_unmute(msg: Message) -> None:
    if not msg.reply_to_message:
        await msg.reply("Используйте в ответ на сообщение")
        return
    await moderation_service.unmute_user(msg, msg.reply_to_message.from_user)


@router.message(F.text.startswith("!kick"))
async def cmd_kick(msg: Message) -> None:
    if not msg.reply_to_message:
        await msg.reply("Используйте в ответ на сообщение")
        return
    reason = msg.text.partition(" ")[2] or "Без причины"
    await moderation_service.kick_user(msg, msg.reply_to_message.from_user, reason)


@router.message(F.text.startswith("!unban"))
async def cmd_unban(msg: Message) -> None:
    parts = msg.text.split(maxsplit=2)
    if len(parts) < 2:
        await msg.reply("Укажите ID пользователя")
        return
    try:
        user_id = int(parts[1])
    except ValueError:
        await msg.reply("Неверный ID")
        return
    await moderation_service.unban_user(msg, user_id)
