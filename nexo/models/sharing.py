from __future__ import annotations

from sqlalchemy import BigInteger, Boolean, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nexo.db.base import Base


class Sharing(Base):
    __tablename__ = "sharing"
    __table_args__ = (Index("ix_sharing_enabled", "enabled"),)

    id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("boards.id", ondelete="CASCADE", name="fk_sharing_board"),
        primary_key=True,
    )
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    token: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    modified_by: Mapped[str | None] = mapped_column(
        Text,
        ForeignKey("users.id", ondelete="SET NULL", name="fk_sharing_modified_by"),
        nullable=True,
    )
    update_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    create_at: Mapped[int] = mapped_column(BigInteger, nullable=False)

    board: Mapped["Board"] = relationship("Board", back_populates="sharing")
    modified_by_user: Mapped["User | None"] = relationship(
        "User",
        foreign_keys=lambda: [Sharing.modified_by],
        viewonly=True,
    )
