from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from sentinelmod.db.base import Base

class ChatSetting(Base):
    __tablename__ = "chat_settings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    key: Mapped[str] = mapped_column(String(50))
    value: Mapped[str] = mapped_column(Text)
