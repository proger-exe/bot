from aiogram import types

from aiogram.utils import exceptions

async def ban_moder(msg: types.Message):
    try:
        user = await msg.bot.get_chat_member(msg.chat.id, msg.reply_to_message.from_id)

        if user.is_chat_admin():
            await msg.reply("Че, ебанулся? Я админа не смогу забанить.")

            return

        await msg.bot.kick_chat_member(chat_id=msg.chat.id, user_id=msg.reply_to_message.from_id)

        await msg.answer(f"Пользователь {msg.reply_to_message.from_user.full_name} был забанен!")

    except exceptions.BadRequest:
        await msg.answer("Пользователя нет или что-то не так..")

async def mute_moder(msg: types.Message):
    try:
        user = await msg.bot.get_chat_member(msg.chat.id, msg.reply_to_message.from_id)

        if user.is_chat_admin():
            await msg.answer("Щас бы админа мутить, м...")

            return 
        
        await msg.bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_id, types.ChatPermissions(False))

        await msg.answer(f"Пользователь {msg.reply_to_message.from_user.full_name} был замучен!")

    
    except exceptions.BadRequest:
        await msg.answer("Пользователя нет или что-то не так..")   

async def unban_moder(msg: types.Message):
    try:
        await msg.bot.unban_chat_member(msg.chat.id, msg.reply_to_message.from_id)

        await msg.answer(f"Пользователь {msg.reply_to_message.from_user.full_name} разбанен!")
    
    except exceptions.BadRequest:
        await msg.answer("Пользователя нет или что-то не так..")

async def unmute_moder(msg: types.Message):

    try:
        await msg.bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_id, types.ChatPermissions(True))

        await msg.answer(f"Пользователь {msg.reply_to_message.from_user.full_name} был размучен!")

    except exceptions.BadRequest:
        await msg.answer("Пользователя нет или что-то не так..")
