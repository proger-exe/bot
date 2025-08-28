import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from sentinelmod.config import settings
from sentinelmod.handlers import register_all_handlers
from sentinelmod.utils.logging import setup_logging

async def main() -> None:
    setup_logging()
    bot = Bot(token=settings.bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    register_all_handlers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
