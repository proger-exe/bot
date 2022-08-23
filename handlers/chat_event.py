from aiogram import types

async def my_member(me: types.ChatMemberUpdated):
    await me.bot.send_message(me.chat.id, "Спасибо за добавление в чат! Для работы мне необходим пост администратора.")

async def new_member(msg: types.Message):
    await msg.answer(f"<b>Привествую тебя, {msg.from_user.first_name},</b> в нашем уютном чате. Прошу тебя прочитать правила по команде /rules")

async def left_member(msg: types.Message):
    await msg.reply("Прощай, я буду скучать.")
