from aiogram import types

async def bot_trigger(msg: types.Message):
    await msg.answer("Да-да, слушаю.")