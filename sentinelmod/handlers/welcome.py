from aiogram import Router, F
from aiogram.types import ChatMemberUpdated

from sentinelmod.services.welcome import process_new_member

router = Router()

@router.chat_member()
async def on_user_join(event: ChatMemberUpdated) -> None:
    if event.new_chat_member.user.is_bot:
        return
    await process_new_member(event)
