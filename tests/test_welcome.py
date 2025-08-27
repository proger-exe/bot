import os
import pytest

os.environ.setdefault("BOT_TOKEN", "test")
os.environ.setdefault("POSTGRES_DSN", "sqlite+aiosqlite:///:memory:")

from aiogram.types import Chat, User

from sentinelmod.db.base import Base, engine
from sentinelmod.services.registration import register_chat
from sentinelmod.services.welcome import (
    get_welcome_settings,
    render_welcome_text,
    set_welcome_captcha,
    set_welcome_photo,
    set_welcome_text,
)


@pytest.mark.asyncio
async def test_render_welcome_text():
    chat = Chat(id=1, type="supergroup", title="Test Chat")
    user = User(id=5, is_bot=False, first_name="John", last_name="Doe", username="jd")
    template = "Hello {user_mention} to {chat_title}!"
    rendered = render_welcome_text(template, user, chat)
    assert user.full_name in rendered
    assert chat.title in rendered


@pytest.mark.asyncio
async def test_welcome_settings_persist():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    chat = Chat(id=100, type="supergroup", title="Persist Chat")

    await set_welcome_text(chat, "Welcome!")
    await set_welcome_photo(chat, "photo123")
    await set_welcome_captcha(chat, True)

    db_chat = await register_chat(chat)
    settings = await get_welcome_settings(db_chat.id)

    assert settings is not None
    assert settings.text_template == "Welcome!"
    assert settings.media_id == "photo123"
    assert settings.require_captcha is True
