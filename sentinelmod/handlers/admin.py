
from aiogram import F, Router
from aiogram.types import Message

from sentinelmod.services.roles import set_user_role
from sentinelmod.services.welcome import (
    set_welcome_captcha,
    set_welcome_photo,
    set_welcome_text,
)
from sentinelmod.services.settings import get_chat_settings, set_chat_setting
from sentinelmod.services.filters import add_stop_word, list_stop_words, remove_stop_word
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


@router.message(F.text.startswith("!settings"))
async def settings_cmd(msg: Message) -> None:
    """Display or edit chat settings."""
    parts = msg.text.split(maxsplit=2)
    if len(parts) == 1:
        cfg = await get_chat_settings(msg.chat)
        if not cfg:
            await msg.reply("Настройки не заданы")
        else:
            lines = [f"{k}: {v}" for k, v in cfg.items()]
            await msg.reply("\n".join(lines))
        return
    if len(parts) < 3:
        await msg.reply("Использование: !settings [key value]")
        return
    key, value = parts[1], parts[2]
    await set_chat_setting(msg.chat, key, value)
    await msg.reply("Настройка сохранена")


@router.message(F.text.startswith("!add_filter"))
async def add_filter_cmd(msg: Message) -> None:
    """Manage stop words for chat."""
    parts = msg.text.split(maxsplit=2)
    if len(parts) == 1:
        words = await list_stop_words(msg.chat)
        if words:
            await msg.reply("Стоп-слова: " + ", ".join(words))
        else:
            await msg.reply("Стоп-слов нет")
        return
    if parts[1] == "remove" and len(parts) == 3:
        await remove_stop_word(msg.chat, parts[2])
        await msg.reply("Стоп-слово удалено")
        return
    if msg.from_user:
        await add_stop_word(msg.chat, msg.from_user, parts[1])
        await msg.reply("Стоп-слово добавлено")
    else:
        await msg.reply("Неизвестный пользователь")

