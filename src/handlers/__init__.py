from aiogram import Dispatcher

from .start import start_handler
from .help import help_handler

from .chat_event import new_member, left_member, my_member

from .features import bot_trigger

from .roleplay import pants_rp, kill_rp, fuck_rp, kiss_rp, butt_pad_rp, masturbate_rp
from .admins import ban_moder, mute_moder, kick_moder, unban_moder, unmute_moder

def setup(dp: Dispatcher):
    "регистрация базовых команд"
    
    dp.register_message_handler(start_handler, commands="start")
    dp.register_message_handler(help_handler, commands="help") 

    "регистрация чат-евентов (вход, выход, добавление и т.д)"

    dp.register_my_chat_member_handler(my_member)

    dp.register_message_handler(new_member, content_types="new_chat_members")
    dp.register_message_handler(left_member, content_types="left_chat_member")

    "Всякие фичи"

    dp.register_message_handler(bot_trigger, text=["Бот", "бот"]) #мне было лень писать что то лучше.

    "рп команды"

    dp.register_message_handler(pants_rp, is_reply=True, text=["Снять штаны", "снять штаны"])
    dp.register_message_handler(kill_rp, is_reply=True, text=["убить", "Убить"])
    dp.register_message_handler(fuck_rp, is_reply=True, text=["Выебать", "выебать", "Трахнуть", "трахнуть"])
    dp.register_message_handler(kiss_rp, is_reply=True, text=["Поцеловать", "поцеловать"])
    dp.register_message_handler(butt_pad_rp, is_reply=True, text=["Чапалах", "чапалах"])
    dp.register_message_handler(masturbate_rp, text=["подрочить", "Подрочить"])
    
    "модерация"

    dp.register_message_handler(ban_moder, is_reply=True, is_admin=True, commands=["ban", "бан"], commands_prefix="!")
    dp.register_message_handler(unban_moder, is_reply=True, is_admin=True, commands=["unban", "разбан"], commands_prefix="!")
    
    dp.register_message_handler(mute_moder, is_reply=True, is_admin=True, commands=["mute", "мут"], commands_prefix="!")
    dp.register_message_handler(unmute_moder, is_reply=True, is_admin=True, commands=["unmute", "размут"], commands_prefix="!")

    
