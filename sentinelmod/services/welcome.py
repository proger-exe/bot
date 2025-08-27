from aiogram.types import ChatMemberUpdated

from sentinelmod.services.registration import register_chat, register_user, add_user_to_chat


async def process_new_member(event: ChatMemberUpdated) -> None:
    """Register user/chat and send a simple welcome message."""
    await register_chat(event.chat)
    user = event.new_chat_member.user
    await register_user(user)
    await add_user_to_chat(user.id, event.chat.id)
    await event.answer(f"Добро пожаловать, {user.full_name}!")
