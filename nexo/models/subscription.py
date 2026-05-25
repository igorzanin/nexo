from __future__ import annotations

from sqlalchemy import BigInteger, CheckConstraint, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column

from nexo.db.base import Base


class Subscription(Base):
    __tablename__ = "subscriptions"
    __table_args__ = (
        CheckConstraint("subscriber_type = 'user'", name="ck_subscriptions_subscriber_type_user"),
        CheckConstraint("publish_at >= 0", name="ck_subscriptions_publish_at_non_negative"),
        Index("ix_subscriptions_subscriber_id", "subscriber_id"),
        Index("ix_subscriptions_block", "block_id", "block_type"),
    )

    block_type: Mapped[str] = mapped_column(Text, primary_key=True)
    block_id: Mapped[str] = mapped_column(Text, primary_key=True)
    subscriber_type: Mapped[str] = mapped_column(Text, primary_key=True)
    subscriber_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("users.id", ondelete="CASCADE", name="fk_subscriptions_user"),
        primary_key=True,
    )
    notify_frequency: Mapped[str | None] = mapped_column(Text, nullable=True)
    create_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    publish_at: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)


class NotificationHint(Base):
    __tablename__ = "notification_hints"
    __table_args__ = (
        CheckConstraint("modify_at >= 0", name="ck_notification_hints_modify_at_non_negative"),
        Index("ix_notification_hints_modify_at", "modify_at"),
    )

    block_type: Mapped[str] = mapped_column(Text, primary_key=True)
    block_id: Mapped[str] = mapped_column(Text, primary_key=True)
    create_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    modify_at: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
