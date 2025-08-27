import os
import pytest
from sqlalchemy import select

os.environ.setdefault("BOT_TOKEN", "test")
os.environ.setdefault("POSTGRES_DSN", "sqlite+aiosqlite:///:memory:")

from aiogram.types import Chat, User

from sentinelmod.db.base import Base, engine, async_session
from sentinelmod.db.models.user import User as UserModel
from sentinelmod.db.models.chat import Chat as ChatModel
from sentinelmod.db.models.user_chat_association import UserChatAssociation
from sentinelmod.services.registration import register_chat, register_user, add_user_to_chat


@pytest.mark.asyncio
async def test_registration_creates_records():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    chat = Chat(id=1, type="supergroup", title="Test Chat")
    user = User(id=10, is_bot=False, first_name="Test", last_name=None, username="user")

    await register_chat(chat)
    await register_user(user)
    await add_user_to_chat(user.id, chat.id)

    async with async_session() as session:
        db_user = await session.scalar(select(UserModel).where(UserModel.tg_id == user.id))
        db_chat = await session.scalar(select(ChatModel).where(ChatModel.tg_id == chat.id))
        link = await session.scalar(
            select(UserChatAssociation).where(
                UserChatAssociation.user_id == db_user.id,
                UserChatAssociation.chat_id == db_chat.id,
            )
        )

    assert db_user is not None
    assert db_chat is not None
    assert link is not None
