import os
import pytest

os.environ.setdefault("BOT_TOKEN", "test")
os.environ.setdefault("POSTGRES_DSN", "sqlite+aiosqlite:///:memory:")

from aiogram.types import Chat, User

from sentinelmod.db.base import Base, engine
from sentinelmod.services.settings import get_chat_settings, set_chat_setting
from sentinelmod.services.filters import add_stop_word, list_stop_words, remove_stop_word


@pytest.mark.asyncio
async def test_chat_settings_persist():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    chat = Chat(id=200, type="supergroup", title="Config Chat")

    await set_chat_setting(chat, "language", "en")
    await set_chat_setting(chat, "timezone", "UTC")

    cfg = await get_chat_settings(chat)

    assert cfg["language"] == "en"
    assert cfg["timezone"] == "UTC"


@pytest.mark.asyncio
async def test_stop_words_persist():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    chat = Chat(id=300, type="supergroup", title="Filter Chat")
    user = User(id=10, is_bot=False, first_name="Tester")

    await add_stop_word(chat, user, "spam")
    words = await list_stop_words(chat)
    assert "spam" in words

    await remove_stop_word(chat, "spam")
    words = await list_stop_words(chat)
    assert "spam" not in words
