from datetime import datetime, timedelta
from sqlalchemy import ForeignKey, String, Text, DateTime, Interval, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from sentinelmod.db.base import Base

class ModerationLog(Base):
    __tablename__ = "moderation_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    moderator_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    action: Mapped[str] = mapped_column(String(20))
    reason: Mapped[str | None] = mapped_column(Text)
    duration: Mapped[timedelta | None] = mapped_column(Interval)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
