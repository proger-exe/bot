"""Stop word management services."""

from aiogram.types import Chat, User
from sqlalchemy import delete, select

from sentinelmod.db.base import async_session
from sentinelmod.db.models.filter_trigger import FilterTrigger
from sentinelmod.services.registration import register_chat, register_user


async def add_stop_word(chat: Chat, user: User, word: str) -> None:
    """Add stop word for chat."""
    db_chat = await register_chat(chat)
    db_user = await register_user(user)
    async with async_session() as session:
        trigger = FilterTrigger(
            chat_id=db_chat.id,
            type="stop_word",
            pattern=word,
            action="delete",
            created_by=db_user.id,
        )
        session.add(trigger)
        await session.commit()


async def remove_stop_word(chat: Chat, word: str) -> None:
    """Remove stop word for chat."""
    db_chat = await register_chat(chat)
    async with async_session() as session:
        await session.execute(
            delete(FilterTrigger).where(
                FilterTrigger.chat_id == db_chat.id,
                FilterTrigger.type == "stop_word",
                FilterTrigger.pattern == word,
            )
        )
        await session.commit()


async def list_stop_words(chat: Chat) -> list[str]:
    """List stop words for chat."""
    db_chat = await register_chat(chat)
    async with async_session() as session:
        result = await session.scalars(
            select(FilterTrigger.pattern).where(
                FilterTrigger.chat_id == db_chat.id,
                FilterTrigger.type == "stop_word",
            )
        )
        return list(result)
