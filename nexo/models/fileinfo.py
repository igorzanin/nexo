from __future__ import annotations

import uuid

from sqlalchemy import BigInteger, Boolean, CheckConstraint, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nexo.db.base import Base


class FileInfo(Base):
    __tablename__ = "file_info"
    __table_args__ = (
        CheckConstraint("delete_at >= 0", name="ck_file_info_delete_at_non_negative"),
        CheckConstraint("size IS NULL OR size >= 0", name="ck_file_info_size_non_negative"),
        Index("ix_file_info_board_id_delete_at", "board_id", "delete_at"),
        Index("ix_file_info_creator_id", "creator_id"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    creator_id: Mapped[str | None] = mapped_column(
        Text,
        ForeignKey("users.id", ondelete="SET NULL", name="fk_file_info_creator"),
        nullable=True,
    )
    board_id: Mapped[str | None] = mapped_column(
        Text,
        ForeignKey("boards.id", ondelete="SET NULL", name="fk_file_info_board"),
        nullable=True,
    )
    create_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    update_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    delete_at: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    path: Mapped[str | None] = mapped_column(Text, nullable=True)
    name: Mapped[str | None] = mapped_column(Text, nullable=True)
    extension: Mapped[str | None] = mapped_column(Text, nullable=True)
    size: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    mime_type: Mapped[str | None] = mapped_column(Text, nullable=True)
    has_preview_image: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    board: Mapped["Board | None"] = relationship("Board", back_populates="files")
    creator: Mapped["User | None"] = relationship(
        "User",
        foreign_keys=lambda: [FileInfo.creator_id],
        viewonly=True,
    )
