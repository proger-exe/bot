from aiogram import F, Router
from aiogram.types import Message

from sentinelmod.services.roles import set_user_role

router = Router()


@router.message(F.text.startswith("!set_admin"))
async def set_admin(msg: Message) -> None:
    """Promote replied user to moderator."""
    if not msg.reply_to_message:
        await msg.reply("Команда должна быть ответом на сообщение пользователя")
        return
    target = msg.reply_to_message.from_user
    await set_user_role(target.id, msg.chat.id, "moderator")
    await msg.reply("Пользователь назначен модератором")
