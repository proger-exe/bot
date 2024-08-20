import random

from aiogram import types

from utils import messager

async def pants_rp(msg: types.Message):
    await msg.answer(messager.get_html("снял(а) штаны у", msg))

async def kill_rp(msg: types.Message):
    await msg.answer(messager.get_html("убил(а)", msg))

async def fuck_rp(msg: types.Message):
    await msg.answer(messager.get_html("принудил(а) к интиму", msg))

async def kiss_rp(msg: types.Message):
    await msg.answer(messager.get_html("поцеловал(а)", msg))

async def butt_pad_rp(msg: types.Message):
    await msg.answer(messager.get_html("дал(а) чапалах", msg))
