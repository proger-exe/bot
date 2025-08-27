from aiogram.types import ChatMemberUpdated

async def process_new_member(event: ChatMemberUpdated) -> None:
    """Send a simple welcome message. Placeholder implementation."""
    await event.answer(f"Добро пожаловать, {event.new_chat_member.user.full_name}!")
