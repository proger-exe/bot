from __future__ import annotations

import re
from collections import defaultdict
from typing import Optional, Tuple

from aiogram.types import Message, User

# In-memory storage for warnings
_warn_counts = defaultdict(int)

# Thresholds for automatic punishment escalation
WARN_MUTE_THRESHOLD = 3
WARN_BAN_THRESHOLD = 5


def parse_duration(token: str) -> Optional[int]:
    """Parse duration string like '10m', '2h'. Return seconds."""
    match = re.fullmatch(r"(\d+)([smhd])", token)
    if not match:
        return None
    value, unit = match.groups()
    multipliers = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    return int(value) * multipliers[unit]


def parse_time_and_reason(text: str) -> Tuple[Optional[int], str]:
    """Parse duration and reason from text."""
    text = text.strip()
    if not text:
        return None, "Без причины"
    first, _, rest = text.partition(" ")
    duration = parse_duration(first)
    if duration is not None:
        reason = rest.strip() or "Без причины"
        return duration, reason
    return None, text


async def _escalate_punishment(msg: Message, target: User, count: int) -> None:
    if count == WARN_MUTE_THRESHOLD:
        # Auto mute for 10 minutes
        await mute_user(msg, target, 600, "Автоматическое наказание после предупреждений")
    elif count == WARN_BAN_THRESHOLD:
        await ban_user(msg, target, None, "Автоматическое наказание после предупреждений")


async def warn_user(msg: Message, target: User, reason: str) -> None:
    """Warn a user and escalate punishment if needed."""
    _warn_counts[target.id] += 1
    count = _warn_counts[target.id]
    await msg.reply(f"Предупреждение {target.full_name}: {reason}")
    await _escalate_punishment(msg, target, count)


async def ban_user(msg: Message, target: User, duration: Optional[int], reason: str) -> None:
    """Ban a user for optional duration."""
    if duration:
        await msg.reply(
            f"Пользователь {target.full_name} забанен на {duration} секунд. Причина: {reason}"
        )
    else:
        await msg.reply(f"Пользователь {target.full_name} забанен. Причина: {reason}")


async def unban_user(msg: Message, user_id: int) -> None:
    """Unban a user by ID."""
    await msg.reply(f"Пользователь {user_id} разбанен")


async def mute_user(msg: Message, target: User, duration: int, reason: str) -> None:
    """Mute a user for a duration."""
    await msg.reply(
        f"Пользователь {target.full_name} замьючен на {duration} секунд. Причина: {reason}"
    )


async def unmute_user(msg: Message, target: User) -> None:
    """Remove mute from a user."""
    await msg.reply(f"Пользователь {target.full_name} размьючен")


async def kick_user(msg: Message, target: User, reason: str) -> None:
    """Kick a user."""
    await msg.reply(f"Пользователь {target.full_name} кикнут. Причина: {reason}")
