import asyncio
import logging

from aiogram import Bot, Dispatcher

from handlers import setup
from utils import config

from filters import IsAdminFilter, IsReplied

def main():
    token = config.get("bot-token")

    bot = Bot(token=token, parse_mode="html")
    dp = Dispatcher(bot)

    logging.basicConfig(level=logging.INFO)

    dp.filters_factory.bind(IsAdminFilter)
    dp.filters_factory.bind(IsReplied)

    setup(dp)

    asyncio.run(dp.start_polling())

if __name__ == "__main__":
    main()