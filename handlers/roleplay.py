import random

from aiogram import types

from utils import messager

async def pants_rp(msg: types.Message):
    await msg.answer(messager.get_html("снял(а) штаны у", msg))

async def kill_rp(msg: types.Message):
    await msg.answer(messager.get_html("убил(а)", msg))

async def fuck_rp(msg: types.Message):
    await msg.answer(messager.get_html("выебал(а)", msg))

async def kiss_rp(msg: types.Message):
    await msg.answer(messager.get_html("поцеловал(а)", msg))

async def butt_pad_rp(msg: types.Message):
    await msg.answer(messager.get_html("дал(а) чапалах", msg))

async def masturbate_rp(msg: types.Message):
    await msg.answer(f"<a href='tg://user?id={msg.from_id}'>{msg.from_user.full_name}</a> дико подрочил(а) и кончил {random.randint(0, 100)}мл. спермы")