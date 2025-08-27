from aiogram.types import Message, User

async def warn_user(msg: Message, target: User, reason: str) -> None:
    """Warn a user. Placeholder implementation."""
    await msg.reply(f"Предупреждение {target.full_name}: {reason}")

async def ban_user(msg: Message, target: User) -> None:
    """Ban a user. Placeholder implementation."""
    await msg.reply(f"Пользователь {target.full_name} забанен")
