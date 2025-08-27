
from aiogram import F, Router
from aiogram.types import Message

from sentinelmod.services.roles import set_user_role
from sentinelmod.services.welcome import (
    set_welcome_captcha,
    set_welcome_photo,
    set_welcome_text,
)
from sentinelmod.handlers.middleware.role_check import RoleCheckMiddleware

router = Router()
router.message.middleware(RoleCheckMiddleware("moderator"))


@router.message(F.text.startswith("!set_admin"))
async def set_admin(msg: Message) -> None:
    """Promote replied user to moderator."""
    if not msg.reply_to_message:
        await msg.reply("Команда должна быть ответом на сообщение пользователя")
        return
    target = msg.reply_to_message.from_user
    await set_user_role(target.id, msg.chat.id, "moderator")
    await msg.reply("Пользователь назначен модератором")


@router.message(F.text.startswith("!set_welcome_photo"))
async def set_welcome_photo_cmd(msg: Message) -> None:
    """Save photo from replied message as welcome image."""
    if not msg.reply_to_message or not msg.reply_to_message.photo:
        await msg.reply("Команда должна быть ответом на сообщение с фото")
        return
    file_id = msg.reply_to_message.photo[-1].file_id
    await set_welcome_photo(msg.chat, file_id)
    await msg.reply("Фото приветствия сохранено")


@router.message(F.text.startswith("!set_welcome_captcha"))
async def set_welcome_captcha_cmd(msg: Message) -> None:
    """Enable or disable captcha requirement."""
    parts = msg.text.split(maxsplit=1)
    if len(parts) < 2 or parts[1] not in {"on", "off"}:
        await msg.reply("Использование: !set_welcome_captcha on|off")
        return
    await set_welcome_captcha(msg.chat, parts[1] == "on")
    await msg.reply("CAPTCHA " + ("включена" if parts[1] == "on" else "выключена"))


@router.message(F.text.startswith("!set_welcome"))
async def set_welcome_cmd(msg: Message) -> None:
    """Set welcome text template."""
    text = msg.text.removeprefix("!set_welcome").strip()
    if not text:
        await msg.reply("Укажите текст приветствия")
        return
    await set_welcome_text(msg.chat, text)
    await msg.reply("Текст приветствия сохранён")

