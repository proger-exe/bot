from datetime import datetime
from sqlalchemy import ForeignKey, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from sentinelmod.db.base import Base

class Federation(Base):
    __tablename__ = "federations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

class FederationChat(Base):
    __tablename__ = "federation_chats"

    federation_id: Mapped[int] = mapped_column(ForeignKey("federations.id"), primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), primary_key=True)

class FederationBan(Base):
    __tablename__ = "federation_bans"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    federation_id: Mapped[int] = mapped_column(ForeignKey("federations.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    reason: Mapped[str | None] = mapped_column(Text)
    global_moderator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
