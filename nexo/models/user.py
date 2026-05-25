from __future__ import annotations

import uuid

from sqlalchemy import BigInteger, Boolean, CheckConstraint, Index, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nexo.db.base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("length(trim(username)) > 0", name="ck_users_username_not_blank"),
        CheckConstraint("length(trim(email)) > 0", name="ck_users_email_not_blank"),
        CheckConstraint("delete_at >= 0", name="ck_users_delete_at_non_negative"),
        Index("ix_users_delete_at", "delete_at"),
        Index("ix_users_email_delete_at", "email", "delete_at"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    username: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    is_bot: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    props: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    create_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    update_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    delete_at: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)

    sessions: Mapped[list["Session"]] = relationship(
        "Session",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    board_memberships: Mapped[list["BoardMember"]] = relationship(
        "BoardMember",
        back_populates="user",
    )
    team_memberships: Mapped[list["TeamMember"]] = relationship(
        "TeamMember",
        back_populates="user",
    )
    categories: Mapped[list["Category"]] = relationship(
        "Category",
        back_populates="user",
    )
    preferences: Mapped[list["Preference"]] = relationship(
        "Preference",
        back_populates="user",
        cascade="all, delete-orphan",
    )
