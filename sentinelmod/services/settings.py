"""Chat settings storage."""

from aiogram.types import Chat
from sqlalchemy import select

from sentinelmod.db.base import async_session
from sentinelmod.db.models.chat_setting import ChatSetting
from sentinelmod.services.registration import register_chat


async def get_chat_settings(chat: Chat) -> dict[str, str]:
    """Return mapping of chat settings."""
    db_chat = await register_chat(chat)
    async with async_session() as session:
        result = await session.scalars(
            select(ChatSetting).where(ChatSetting.chat_id == db_chat.id)
        )
        return {row.key: row.value for row in result}


async def set_chat_setting(chat: Chat, key: str, value: str) -> None:
    """Store single chat setting."""
    db_chat = await register_chat(chat)
    async with async_session() as session:
        row = await session.scalar(
            select(ChatSetting).where(
                ChatSetting.chat_id == db_chat.id, ChatSetting.key == key
            )
        )
        if row:
            row.value = value
        else:
            session.add(ChatSetting(chat_id=db_chat.id, key=key, value=value))
        await session.commit()
