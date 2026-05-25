from __future__ import annotations

import uuid

from sqlalchemy import BigInteger, CheckConstraint, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nexo.db.base import Base


class Session(Base):
    __tablename__ = "sessions"
    __table_args__ = (
        CheckConstraint("expire_at >= create_at", name="ck_sessions_expire_at_gte_create_at"),
        Index("ix_sessions_user_id", "user_id"),
        Index("ix_sessions_expire_at", "expire_at"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    token: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    user_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("users.id", ondelete="CASCADE", name="fk_sessions_user"),
        nullable=False,
    )
    create_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    last_active_time: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    expire_at: Mapped[int] = mapped_column(BigInteger, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="sessions")