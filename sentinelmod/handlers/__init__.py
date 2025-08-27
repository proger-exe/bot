from aiogram import Dispatcher

from . import welcome, moderation, admin

def register_all_handlers(dp: Dispatcher) -> None:
    dp.include_router(welcome.router)
    dp.include_router(moderation.router)
    dp.include_router(admin.router)
