from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardMarkup, \
	InlineKeyboardButton, ReplyKeyboardRemove
from random import randint
import random
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from aiogram.dispatcher.filters import BoundFilter
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware


class IsAdminFilter(BoundFilter):
    key = "is_admin"
    
    def __init__(self, is_admin):
        self.is_admin = is_admin
    
    async def check(self, message: types.Message):
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin()



TOKEN = '1846763082:AAHMJHoMRyrVgd-HT2Z9tAoGJIJB-aqLjB0'#и да это работает
SUCCED = 'Активированно!'


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

dp.filters_factory.bind(IsAdminFilter)

@dp.message_handler(commands=['start'])
async def cmd_test(message: types.Message):
    # You can use this command every 5 seconds
    await message.reply("""Вас приветствует бот
Помощь: /help""")

@dp.message_handler(commands=["rules"])
async def rules(msg: types.Message):
    await msg.reply("https://telegra.ph/Pravila-06-25-8")

@dp.message_handler(commands=["help"])
async def help(msg: types.Message):
    await msg.reply("""<b>❤️ ||Команды для админов|| ❤️ </b>
мут/mute | разглушить/unmute | бан/банан/ban | разбан/unban | удолить/deleate |
<b>❤️ || рп команды || ❤️</b>
снять штаны |выебать | поцеловать""", parse_mode = 'HTML')


@dp.message_handler(content_types=["new_chat_members"])
async def new(message: types.Message):
    await message.reply("Привествую тебя " + message.from_user.first_name + " в нашем уютном чате но прошу тебя прочитать правила /rules")

@dp.message_handler(content_types=["left_chat_member"])
async def left(message: types.Message):
    await message.reply("Уходи уебище, без тебя было лучше.")

@dp.message_handler(Text("Бот",ignore_case=True))
async def pong(msg: types.Message):
    await msg.reply("епт, заебали, я в отпуске...")

@dp.message_handler(is_admin=True, commands=["mute","мут"], commands_prefix="!")
async def mute(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение !")
        return

    user = await message.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    if user.is_chat_admin():
        await message.reply("Не бро, я не буду глушить админа.")
        return
    
    await message.bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions())
    
    await message.reply("Участник заглушен !")

@dp.message_handler(is_admin=True, commands=["unmute","разглушить"], commands_prefix="!")
async def unmute(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение !")
        return
    
    await message.bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(True))
    
    await message.reply(f"ОК. {message.reply_to_message.from_user.first_name} может спокойно говорить, но пусть придержит язык за зубами.")

@dp.message_handler(is_admin=True, commands=["ban","бан"], commands_prefix="!")
async def ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение !")
        return

    user = await message.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    if user.is_chat_admin():
        await message.reply("Не бро, я не буду банить админа.")
        return

    await message.bot.delete_message(message.chat.id, message.message_id)
    await message.bot.kick_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
    
    await message.reply_to_message.reply("Челик забанен !")

@dp.message_handler(is_admin=True, commands=["unban","разбан"], commands_prefix="!")
async def unban(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение !")
        return
    
    await message.bot.unban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
    
    await message.reply_to_message.reply("Челик разбанен и может войти заново !")

@dp.message_handler(is_admin=True, commands=['deleate',"удалить"], commands_prefix="!")
async def delete_message(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение !")
        return

    user = await message.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    if user.is_chat_admin():
        await message.reply("Не бро, я не буду удалять сообщение админа.")
        return

    await message.reply_to_message.delete()
    await message.reply("Сообщение удалено !")

@dp.message_handler(Text("Ебнуть",ignore_case=True))
async def pong(msg: types.Message):
    await msg.reply('💥' + random.choice(ebt))

@dp.message_handler(Text("Ку",ignore_case=True))
async def pong(msg: types.Message):
    await msg.reply(random.choice(ku))

@dp.message_handler(Text("Дрочить",ignore_case=True))
async def pong(msg: types.Message):
    await msg.reply('🔞 Ты кончил за ' + str(randint(0,10000)) + " минут")

@dp.message_handler(Text("выебать",ignore_case=True))
async def sex2(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение !")
        return
    
    await message.answer(f"""<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> трахнул(а) <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>""", parse_mode = "html")

@dp.message_handler(Text("убить",ignore_case=True))
async def sex2(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение !")
        return
    
    await message.answer(f"""<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> убил(а) <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>""", parse_mode = "html")

@dp.message_handler(Text("снять штаны",ignore_case=True))
async def sex2(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение !")
        return
    
    await message.answer(f"""<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> снял(а) штаны у <a href="tg://user?id={message.reply_to_message.from_user.id}">Дауна</a>""", parse_mode = "html")

#Листик фраз 

ku = ['👋 Дарова', '👋 Ку', '👋 Привет', '👋 Салям Алейкум', '👋 Hi!', '👋 Hello', '👋 Шалам']

ebt = ['Ебнул как подушка об лицо, лох', 'Удар отражен, лох, пидр.', 'Отразил', 'Бедный чел, зачем ты его так...']

if __name__ == '__main__':
    executor.start_polling(dp)
