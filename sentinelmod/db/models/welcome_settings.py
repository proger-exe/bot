from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from sentinelmod.db.base import Base


class WelcomeSettings(Base):
    """Store welcome message configuration for a chat."""

    __tablename__ = "welcome_settings"

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), primary_key=True)
    text_template: Mapped[str | None] = mapped_column(Text, nullable=True)
    media_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    require_captcha: Mapped[bool] = mapped_column(Boolean, default=False)
