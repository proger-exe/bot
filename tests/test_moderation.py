import os
import pytest

os.environ.setdefault("BOT_TOKEN", "test")
os.environ.setdefault("POSTGRES_DSN", "sqlite+aiosqlite:///:memory:")

from sentinelmod.services.moderation import parse_duration, parse_time_and_reason


@pytest.mark.parametrize(
    "token,expected",
    [
        ("10m", 600),
        ("1h30m", 5400),
        ("2d5h", 2 * 86400 + 5 * 3600),
        ("2h5m10s", 2 * 3600 + 5 * 60 + 10),
        ("1ч30м", 5400),
        ("2д", 2 * 86400),
        ("bad", None),
    ],
)
async def test_parse_duration(token, expected):
    assert parse_duration(token) == expected


@pytest.mark.parametrize(
    "text, expected_duration, expected_reason",
    [
        ("1h30m test reason", 5400, "test reason"),
        ("1ч30м тест", 5400, "тест"),
    ],
)
@pytest.mark.asyncio
async def test_parse_time_and_reason(text, expected_duration, expected_reason):
    duration, reason = parse_time_and_reason(text)
    assert duration == expected_duration
    assert reason == expected_reason
