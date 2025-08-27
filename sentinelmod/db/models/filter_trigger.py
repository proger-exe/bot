from datetime import datetime, timedelta
from sqlalchemy import ForeignKey, String, Text, Interval, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from sentinelmod.db.base import Base

class FilterTrigger(Base):
    __tablename__ = "filter_triggers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int | None] = mapped_column(ForeignKey("chats.id"))
    type: Mapped[str] = mapped_column(String(20))
    pattern: Mapped[str | None] = mapped_column(Text)
    action: Mapped[str] = mapped_column(String(20))
    action_duration: Mapped[timedelta | None] = mapped_column(Interval)
    action_payload: Mapped[str | None] = mapped_column(Text)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
