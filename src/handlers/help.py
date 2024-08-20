from aiogram import types

async def help_handler(msg: types.Message):
    await msg.reply(
        '<b>❇️ <Команды для админов> ❇️</b>\n'
        "мут/mute - Замутить пользователя (chat-only)\n"
        "размут/unmute - Размутить пользователя (chat-only)\n"
        "бан/ban - Забанить пользователя (chat-only)\n"
        "разбан/unban - Разбанить пользователя (chat-only)\n\n"
        "<b>❇️ <Команды для roleplay> ❇️</b>\n"
        "снять штаны | поцеловать | чапалах (дать чапалах)"
    )
