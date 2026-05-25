from __future__ import annotations

import uuid

from sqlalchemy import BigInteger, Boolean, CheckConstraint, ForeignKey, Index, Integer, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nexo.db.base import Base


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (
        CheckConstraint("type IN ('system', 'custom')", name="ck_categories_type_valid"),
        CheckConstraint("delete_at >= 0", name="ck_categories_delete_at_non_negative"),
        Index("ix_categories_user_team_delete_at", "user_id", "team_id", "delete_at"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("users.id", ondelete="CASCADE", name="fk_categories_user"),
        nullable=False,
    )
    team_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("teams.id", ondelete="CASCADE", name="fk_categories_team"),
        nullable=False,
    )
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    type: Mapped[str] = mapped_column(Text, nullable=False, default="custom")
    create_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    update_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    delete_at: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)

    user: Mapped["User"] = relationship("User", back_populates="categories")
    team: Mapped["Team"] = relationship("Team", back_populates="categories")
    boards: Mapped[list["CategoryBoard"]] = relationship("CategoryBoard", back_populates="category")


class CategoryBoard(Base):
    __tablename__ = "category_boards"
    __table_args__ = (
        UniqueConstraint("category_id", "board_id", "user_id", name="uq_category_boards_unique"),
        CheckConstraint("delete_at >= 0", name="ck_category_boards_delete_at_non_negative"),
        Index("ix_category_boards_board_id_delete_at", "board_id", "delete_at"),
        Index("ix_category_boards_category_sort", "category_id", "sort_order"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("users.id", ondelete="CASCADE", name="fk_category_boards_user"),
        nullable=False,
    )
    team_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("teams.id", ondelete="CASCADE", name="fk_category_boards_team"),
        nullable=False,
    )
    category_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("categories.id", ondelete="CASCADE", name="fk_category_boards_category"),
        nullable=False,
    )
    board_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("boards.id", ondelete="CASCADE", name="fk_category_boards_board"),
        nullable=False,
    )
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    hide: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    create_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    update_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    delete_at: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)

    category: Mapped["Category"] = relationship("Category", back_populates="boards")
    board: Mapped["Board"] = relationship("Board", back_populates="board_categories")
    user: Mapped["User | None"] = relationship(
        "User",
        foreign_keys=lambda: [CategoryBoard.user_id],
        viewonly=True,
    )
