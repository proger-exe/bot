from aiogram import Router, F
from aiogram.types import Message

from sentinelmod.services import moderation as moderation_service

router = Router()

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
    await moderation_service.ban_user(msg, msg.reply_to_message.from_user)
