from __future__ import annotations

import re
from collections import defaultdict
from datetime import timedelta
from typing import Optional, Tuple, List

from aiogram.types import Message, User
from sqlalchemy import select

from sentinelmod.db.base import async_session
from sentinelmod.db.models.moderation_log import ModerationLog
from sentinelmod.services.registration import register_chat, register_user

# In-memory storage for warnings
_warn_counts = defaultdict(int)

# Thresholds for automatic punishment escalation
WARN_MUTE_THRESHOLD = 3
WARN_BAN_THRESHOLD = 5


def parse_duration(token: str) -> Optional[int]:
    """Parse duration string into seconds.

    Supports combined values like ``1h30m`` or ``2d5h``. Returns ``None`` if the
    string does not fully match the expected pattern.
    """

    if not token:
        return None

    token = token.lower()

    multipliers = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400,
        "с": 1,
        "м": 60,
        "ч": 3600,
        "д": 86400,
    }

    parts = re.findall(r"(\d+)([smhdсмачд])", token)

    if not parts or "".join(f"{v}{u}" for v, u in parts) != token:
        return None
    return sum(int(value) * multipliers[unit] for value, unit in parts)


def format_duration(seconds: int) -> str:
    """Return a human readable representation of ``seconds``."""

    periods = (("d", 86400, "д"), ("h", 3600, "ч"), ("m", 60, "м"), ("s", 1, "с"))
    remaining = seconds
    parts = []
    for _, length, suffix in periods:
        value, remaining = divmod(remaining, length)
        if value:
            parts.append(f"{value}{suffix}")
    return " ".join(parts) if parts else "0с"


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
    await msg.reply(
        f"Предупреждение {target.full_name}: {reason} (#{count})"
    )
    await _escalate_punishment(msg, target, count)

    await log_action(msg, target, "warn", reason, is_public=True)


async def ban_user(msg: Message, target: User, duration: Optional[int], reason: str) -> None:
    """Ban a user for optional duration."""
    if duration:
        await msg.reply(
            f"Пользователь {target.full_name} забанен на {format_duration(duration)}. Причина: {reason}"
        )
    else:
        await msg.reply(f"Пользователь {target.full_name} забанен. Причина: {reason}")

    await log_action(msg, target, "ban", reason, duration)


async def unban_user(msg: Message, user_id: int) -> None:
    """Unban a user by ID."""
    await msg.reply(f"Пользователь {user_id} разбанен")

    if msg.from_user:
        # Log unban if moderator info is available
        await log_action(msg, User(id=user_id, is_bot=False, first_name=""), "unban", None)


async def mute_user(msg: Message, target: User, duration: int, reason: str) -> None:
    """Mute a user for a duration."""
    await msg.reply(
        f"Пользователь {target.full_name} замьючен на {format_duration(duration)}. Причина: {reason}"
    )

    await log_action(msg, target, "mute", reason, duration)


async def unmute_user(msg: Message, target: User) -> None:
    """Remove mute from a user."""
    await msg.reply(f"Пользователь {target.full_name} размьючен")

    await log_action(msg, target, "unmute", None)


async def kick_user(msg: Message, target: User, reason: str) -> None:
    """Kick a user."""
    await msg.reply(f"Пользователь {target.full_name} кикнут. Причина: {reason}")

    await log_action(msg, target, "kick", reason)


async def log_action(
    msg: Message,
    target: User,
    action: str,
    reason: str | None = None,
    duration: int | None = None,
    is_public: bool = False,
) -> None:
    """Store moderation action in ModerationLog."""

    db_chat = await register_chat(msg.chat)
    db_target = await register_user(target)
    moderator_id = None
    if msg.from_user:
        db_moderator = await register_user(msg.from_user)
        moderator_id = db_moderator.id

    async with async_session() as session:
        entry = ModerationLog(
            chat_id=db_chat.id,
            user_id=db_target.id,
            moderator_id=moderator_id,
            action=action,
            reason=reason,
            duration=timedelta(seconds=duration) if duration else None,
            is_public=is_public,
        )
        session.add(entry)
        await session.commit()


async def get_logs(
    chat_id: int, user_id: int, public_only: bool = False
) -> List[ModerationLog]:
    """Fetch moderation logs for a user."""

    async with async_session() as session:
        stmt = select(ModerationLog).where(
            ModerationLog.chat_id == chat_id, ModerationLog.user_id == user_id
        )
        if public_only:
            stmt = stmt.where(ModerationLog.is_public.is_(True))
        stmt = stmt.order_by(ModerationLog.created_at.desc())
        result = await session.scalars(stmt)
        return list(result)
