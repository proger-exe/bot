"""User and chat registration helpers."""

from aiogram.types import Chat, User as TGUser
from sqlalchemy import select

from sentinelmod.db.base import async_session
from sentinelmod.db.models.chat import Chat as ChatModel
from sentinelmod.db.models.user import User as UserModel
from sentinelmod.db.models.user_chat_association import UserChatAssociation


async def register_chat(chat: Chat) -> ChatModel:
    """Ensure chat exists in database."""
    async with async_session() as session:
        db_chat = await session.scalar(select(ChatModel).where(ChatModel.tg_id == chat.id))
        if db_chat:
            return db_chat
        db_chat = ChatModel(tg_id=chat.id, title=chat.title or "")
        session.add(db_chat)
        await session.commit()
        return db_chat


async def register_user(user: TGUser) -> UserModel:
    """Ensure user exists in database."""
    async with async_session() as session:
        db_user = await session.scalar(select(UserModel).where(UserModel.tg_id == user.id))
        if db_user:
            return db_user
        db_user = UserModel(
            tg_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        session.add(db_user)
        await session.commit()
        return db_user


async def add_user_to_chat(user_id: int, chat_id: int) -> None:
    """Create association between user and chat if not exists."""
    async with async_session() as session:
        link = await session.scalar(
            select(UserChatAssociation)
            .where(UserChatAssociation.user_id == user_id, UserChatAssociation.chat_id == chat_id)
        )
        if link:
            return
        session.add(UserChatAssociation(user_id=user_id, chat_id=chat_id))
        await session.commit()
