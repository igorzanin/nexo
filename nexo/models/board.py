from __future__ import annotations

import uuid

from sqlalchemy import BigInteger, Boolean, CheckConstraint, ForeignKey, Index, Integer, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nexo.db.base import Base


class Board(Base):
    __tablename__ = "boards"
    __table_args__ = (
        CheckConstraint("type IN ('O', 'P')", name="ck_boards_type_valid"),
        CheckConstraint(
            "minimum_role IN ('', 'viewer', 'commenter', 'editor', 'admin')",
            name="ck_boards_minimum_role_valid",
        ),
        CheckConstraint("delete_at >= 0", name="ck_boards_delete_at_non_negative"),
        CheckConstraint("template_version >= 0", name="ck_boards_template_version_non_negative"),
        Index("ix_boards_team_id_delete_at", "team_id", "delete_at"),
        Index("ix_boards_created_by", "created_by"),
        Index("ix_boards_type_delete_at", "type", "delete_at"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    team_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("teams.id", ondelete="RESTRICT", name="fk_boards_team"),
        nullable=False,
    )
    created_by: Mapped[str | None] = mapped_column(
        Text,
        ForeignKey("users.id", ondelete="SET NULL", name="fk_boards_created_by"),
        nullable=True,
    )
    modified_by: Mapped[str | None] = mapped_column(
        Text,
        ForeignKey("users.id", ondelete="SET NULL", name="fk_boards_modified_by"),
        nullable=True,
    )
    type: Mapped[str] = mapped_column(Text, nullable=False, default="P")
    minimum_role: Mapped[str] = mapped_column(Text, nullable=False, default="")
    title: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    icon: Mapped[str | None] = mapped_column(Text, nullable=True)
    show_description: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_template: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    template_version: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    properties: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    card_properties: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    create_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    update_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    delete_at: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)

    team: Mapped["Team"] = relationship("Team", back_populates="boards")
    blocks: Mapped[list["Block"]] = relationship("Block", back_populates="board")
    sharing: Mapped["Sharing | None"] = relationship(
        "Sharing",
        uselist=False,
        back_populates="board",
    )
    board_members: Mapped[list["BoardMember"]] = relationship(
        "BoardMember",
        back_populates="board",
    )
    board_categories: Mapped[list["CategoryBoard"]] = relationship(
        "CategoryBoard",
        back_populates="board",
    )
    files: Mapped[list["FileInfo"]] = relationship("FileInfo", back_populates="board")


class BoardMember(Base):
    __tablename__ = "board_members"
    __table_args__ = (
        CheckConstraint("delete_at >= 0", name="ck_board_members_delete_at_non_negative"),
        CheckConstraint(
            """
            (CASE WHEN scheme_admin THEN 1 ELSE 0 END) +
            (CASE WHEN scheme_editor THEN 1 ELSE 0 END) +
            (CASE WHEN scheme_commenter THEN 1 ELSE 0 END) +
            (CASE WHEN scheme_viewer THEN 1 ELSE 0 END) <= 1
            """,
            name="ck_board_members_single_scheme",
        ),
        Index("ix_board_members_user_id_delete_at", "user_id", "delete_at"),
    )

    board_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("boards.id", ondelete="CASCADE", name="fk_board_members_board"),
        primary_key=True,
    )
    user_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("users.id", ondelete="CASCADE", name="fk_board_members_user"),
        primary_key=True,
    )
    roles: Mapped[str | None] = mapped_column(Text, nullable=True)
    scheme_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    scheme_editor: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    scheme_commenter: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    scheme_viewer: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    create_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    update_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    delete_at: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)

    board: Mapped["Board"] = relationship("Board", back_populates="board_members")
    user: Mapped["User"] = relationship("User", back_populates="board_memberships")
