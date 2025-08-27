"""Middleware to enforce minimum user roles for handlers."""

from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from sentinelmod.services.roles import DEFAULT_ROLES, get_user_role


class RoleCheckMiddleware(BaseMiddleware):
    """Ensure that user has at least ``min_role`` in the chat."""

    def __init__(self, min_role: str) -> None:
        self.min_role = min_role
        try:
            self._min_index = DEFAULT_ROLES.index(min_role)
        except ValueError:
            raise ValueError(f"Unknown role: {min_role}") from None

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if isinstance(event, Message):
            role = await get_user_role(event.from_user.id, event.chat.id)
            if role is None:
                role_index = 0
            else:
                try:
                    role_index = DEFAULT_ROLES.index(role)
                except ValueError:
                    role_index = 0
            if role_index < self._min_index:
                await event.reply("Недостаточно прав")
                return
        return await handler(event, data)
