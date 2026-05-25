from __future__ import annotations

import uuid

from sqlalchemy import BigInteger, CheckConstraint, ForeignKey, Index, Integer, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nexo.db.base import Base


class Block(Base):
    __tablename__ = "blocks"
    __table_args__ = (
        CheckConstraint("schema >= 1", name="ck_blocks_schema_min"),
        CheckConstraint("delete_at >= 0", name="ck_blocks_delete_at_non_negative"),
        Index("ix_blocks_board_id_delete_at", "board_id", "delete_at"),
        Index("ix_blocks_root_id", "root_id"),
        Index("ix_blocks_parent_id", "parent_id"),
        Index("ix_blocks_type_board_delete_at", "type", "board_id", "delete_at"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    parent_id: Mapped[str | None] = mapped_column(
        Text,
        ForeignKey("blocks.id", ondelete="SET NULL", name="fk_blocks_parent"),
        nullable=True,
    )
    root_id: Mapped[str | None] = mapped_column(
        Text,
        ForeignKey("blocks.id", ondelete="SET NULL", name="fk_blocks_root"),
        nullable=True,
    )
    created_by: Mapped[str | None] = mapped_column(
        Text,
        ForeignKey("users.id", ondelete="SET NULL", name="fk_blocks_created_by"),
        nullable=True,
    )
    modified_by: Mapped[str | None] = mapped_column(
        Text,
        ForeignKey("users.id", ondelete="SET NULL", name="fk_blocks_modified_by"),
        nullable=True,
    )
    schema: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    type: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str | None] = mapped_column(Text, nullable=True)
    fields: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    create_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    update_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    delete_at: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    board_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("boards.id", ondelete="CASCADE", name="fk_blocks_board"),
        nullable=False,
    )

    board: Mapped["Board"] = relationship("Board", back_populates="blocks")
    parent: Mapped["Block | None"] = relationship(
        "Block",
        foreign_keys=lambda: [Block.parent_id],
        remote_side=lambda: [Block.id],
        back_populates="children",
    )
    children: Mapped[list["Block"]] = relationship(
        "Block",
        foreign_keys=lambda: [Block.parent_id],
        back_populates="parent",
    )
    root_block: Mapped["Block | None"] = relationship(
        "Block",
        foreign_keys=lambda: [Block.root_id],
        remote_side=lambda: [Block.id],
        viewonly=True,
    )


class BlockHistory(Base):
    __tablename__ = "blocks_history"
    __table_args__ = (
        CheckConstraint("insert_at >= create_at", name="ck_blocks_history_insert_at_gte_create_at"),
        CheckConstraint("delete_at > 0", name="ck_blocks_history_delete_at_positive"),
        Index("ix_blocks_history_board_id_insert_at", "board_id", "insert_at"),
        Index("ix_blocks_history_delete_at", "delete_at"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    parent_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    root_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[str | None] = mapped_column(
        Text,
        ForeignKey("users.id", ondelete="SET NULL", name="fk_blocks_history_created_by"),
        nullable=True,
    )
    modified_by: Mapped[str | None] = mapped_column(
        Text,
        ForeignKey("users.id", ondelete="SET NULL", name="fk_blocks_history_modified_by"),
        nullable=True,
    )
    schema: Mapped[int | None] = mapped_column(Integer, nullable=True)
    type: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str | None] = mapped_column(Text, nullable=True)
    fields: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    create_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    update_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    delete_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    board_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("boards.id", ondelete="CASCADE", name="fk_blocks_history_board"),
        nullable=False,
    )
    insert_at: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
