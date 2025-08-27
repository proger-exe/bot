"""Welcome message helpers and settings storage."""

from __future__ import annotations

from aiogram.types import Chat, ChatMemberUpdated, User

from sentinelmod.db.base import async_session
from sentinelmod.db.models.welcome_settings import WelcomeSettings
from sentinelmod.services.registration import (
    add_user_to_chat,
    register_chat,
    register_user,
)


async def set_welcome_text(chat: Chat, text: str) -> None:
    """Store welcome text template for a chat."""
    db_chat = await register_chat(chat)
    async with async_session() as session:
        settings = await session.get(WelcomeSettings, db_chat.id)
        if settings:
            settings.text_template = text
        else:
            settings = WelcomeSettings(chat_id=db_chat.id, text_template=text)
            session.add(settings)
        await session.commit()


async def set_welcome_photo(chat: Chat, file_id: str) -> None:
    """Store welcome photo file_id for a chat."""
    db_chat = await register_chat(chat)
    async with async_session() as session:
        settings = await session.get(WelcomeSettings, db_chat.id)
        if settings:
            settings.media_id = file_id
        else:
            settings = WelcomeSettings(chat_id=db_chat.id, media_id=file_id)
            session.add(settings)
        await session.commit()


async def set_welcome_captcha(chat: Chat, enabled: bool) -> None:
    """Enable or disable CAPTCHA challenge for a chat."""
    db_chat = await register_chat(chat)
    async with async_session() as session:
        settings = await session.get(WelcomeSettings, db_chat.id)
        if settings:
            settings.require_captcha = enabled
        else:
            settings = WelcomeSettings(chat_id=db_chat.id, require_captcha=enabled)
            session.add(settings)
        await session.commit()


async def get_welcome_settings(chat_db_id: int) -> WelcomeSettings | None:
    """Retrieve welcome settings for chat by internal DB id."""
    async with async_session() as session:
        return await session.get(WelcomeSettings, chat_db_id)


def render_welcome_text(template: str, user: User, chat: Chat) -> str:
    """Replace placeholders in template with real data."""
    return (
        template.replace("{user_mention}", user.mention_html())
        .replace("{chat_title}", chat.title or "")
    )


async def process_new_member(event: ChatMemberUpdated) -> None:
    """Register user/chat and send welcome message according to settings."""
    db_chat = await register_chat(event.chat)
    user = event.new_chat_member.user
    await register_user(user)
    await add_user_to_chat(user.id, event.chat.id)

    settings = await get_welcome_settings(db_chat.id)
    if not settings or not settings.text_template:
        await event.answer(f"Добро пожаловать, {user.full_name}!")
        return

    text = render_welcome_text(settings.text_template, user, event.chat)

    if settings.media_id:
        await event.bot.send_photo(event.chat.id, settings.media_id, caption=text)
    else:
        await event.answer(text)

    if settings.require_captcha:
        await event.answer("Пожалуйста, подтвердите, что вы человек, ответив '42'.")

