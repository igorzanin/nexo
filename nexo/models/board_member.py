from sqlalchemy import Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nexo.db.base import Base


class BoardMember(Base):
    __tablename__ = "board_members"

    boardId: Mapped[str] = mapped_column(Text, ForeignKey("boards.id"), primary_key=True)
    userId: Mapped[str] = mapped_column(Text, ForeignKey("users.id"), primary_key=True)
    minimumRole: Mapped[str] = mapped_column(Text, nullable=False)
    schemeAdmin: Mapped[bool] = mapped_column(Boolean, nullable=False)
    schemeEditor: Mapped[bool] = mapped_column(Boolean, nullable=False)
    schemeCommenter: Mapped[bool] = mapped_column(Boolean, nullable=False)
    schemeViewer: Mapped[bool] = mapped_column(Boolean, nullable=False)

    board = relationship("Board", back_populates="board_members")
    user = relationship("User", back_populates="board_memberships")
