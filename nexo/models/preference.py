from __future__ import annotations

from sqlalchemy import CheckConstraint, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nexo.db.base import Base


class Preference(Base):
    __tablename__ = "preferences"
    __table_args__ = (
        CheckConstraint("length(trim(category)) > 0", name="ck_preferences_category_not_blank"),
        CheckConstraint("length(trim(name)) > 0", name="ck_preferences_name_not_blank"),
        Index("ix_preferences_user_category", "user_id", "category"),
    )

    user_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("users.id", ondelete="CASCADE", name="fk_preferences_user"),
        primary_key=True,
    )
    category: Mapped[str] = mapped_column(Text, primary_key=True)
    name: Mapped[str] = mapped_column(Text, primary_key=True)
    value: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="preferences")
