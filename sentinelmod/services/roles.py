"""Role management helpers."""

from sqlalchemy import select

from sentinelmod.db.base import async_session
from sentinelmod.db.models.role import Role, UserChatRole


DEFAULT_ROLES = ["member", "moderator", "administrator", "creator"]


async def ensure_default_roles() -> None:
    """Create base roles if they are missing."""
    async with async_session() as session:
        for name in DEFAULT_ROLES:
            exists = await session.scalar(select(Role).where(Role.name == name))
            if not exists:
                session.add(Role(name=name))
        await session.commit()


async def set_user_role(
    user_id: int,
    chat_id: int,
    role_name: str,
    *,
    is_hidden: bool = False,
) -> None:
    """Assign a role to a user within a chat."""
    async with async_session() as session:
        role = await session.scalar(select(Role).where(Role.name == role_name))
        if not role:
            role = Role(name=role_name)
            session.add(role)
            await session.flush()

        assoc = await session.get(
            UserChatRole, {"user_id": user_id, "chat_id": chat_id}
        )
        if assoc:
            assoc.role_id = role.id
            assoc.is_hidden = is_hidden
        else:
            session.add(
                UserChatRole(
                    user_id=user_id,
                    chat_id=chat_id,
                    role_id=role.id,
                    is_hidden=is_hidden,
                )
            )
        await session.commit()


async def get_user_role(user_id: int, chat_id: int) -> str | None:
    """Return role name assigned to user in chat."""
    async with async_session() as session:
        result = await session.execute(
            select(Role.name)
            .join(UserChatRole)
            .where(
                UserChatRole.user_id == user_id,
                UserChatRole.chat_id == chat_id,
            )
        )
        return result.scalar_one_or_none()

