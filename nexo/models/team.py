from __future__ import annotations

import uuid

from sqlalchemy import BigInteger, Boolean, CheckConstraint, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nexo.db.base import Base


class Team(Base):
    __tablename__ = "teams"
    __table_args__ = (
        CheckConstraint("type IN ('O', 'P')", name="ck_teams_type_valid"),
        CheckConstraint("delete_at >= 0", name="ck_teams_delete_at_non_negative"),
        Index("ix_teams_delete_at", "delete_at"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    display_name: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(Text, nullable=False, default="O")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    create_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    update_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    delete_at: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)

    boards: Mapped[list["Board"]] = relationship("Board", back_populates="team")
    members: Mapped[list["TeamMember"]] = relationship("TeamMember", back_populates="team")
    categories: Mapped[list["Category"]] = relationship("Category", back_populates="team")


class TeamMember(Base):
    __tablename__ = "team_members"
    __table_args__ = (
        CheckConstraint("delete_at >= 0", name="ck_team_members_delete_at_non_negative"),
        CheckConstraint(
            "NOT (scheme_guest = TRUE AND scheme_user = TRUE)",
            name="ck_team_members_guest_user_exclusive",
        ),
        CheckConstraint(
            "NOT (scheme_guest = TRUE AND scheme_admin = TRUE)",
            name="ck_team_members_guest_admin_exclusive",
        ),
        Index("ix_team_members_user_id_delete_at", "user_id", "delete_at"),
    )

    team_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("teams.id", ondelete="CASCADE", name="fk_team_members_team"),
        primary_key=True,
    )
    user_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("users.id", ondelete="CASCADE", name="fk_team_members_user"),
        primary_key=True,
    )
    roles: Mapped[str | None] = mapped_column(Text, nullable=True)
    scheme_guest: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    scheme_user: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    scheme_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    create_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    update_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    delete_at: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)

    team: Mapped["Team"] = relationship("Team", back_populates="members")
    user: Mapped["User"] = relationship("User", back_populates="team_memberships")
