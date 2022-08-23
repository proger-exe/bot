from aiogram import types

async def start_handler(msg: types.Message):
    await msg.answer("<b>Добро пожаловать! </b>\n\n"
        "Для обучения работы с ботом пропишите /help.")