from aiogram import types

async def help_handler(msg: types.Message):
    await msg.reply('<b>❤️ ||Команды для админов|| ❤️ </b>\n'
                    "мут/mute | размут/unmute | бан/ban | разбан/unban\n\n"
                    "<b>❤️ || рп команды || ❤️</b>\n"
                    "снять штаны | выебать | поцеловать | чапалах | подрочить")