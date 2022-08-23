from aiogram import types

def get_html(text: str, msg: types.Message):
    return f'<a href="tg://user?id={msg.from_id}">{msg.from_user.full_name}</a> {text} <a href="tg://user?id={msg.reply_to_message.from_id}">{msg.reply_to_message.from_user.full_name}</a>'