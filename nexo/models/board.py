import uuid

from sqlalchemy import Text, BigInteger, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nexo.db.base import Base


class Board(Base):
    __tablename__ = "boards"

    id: Mapped[str] = mapped_column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    teamId: Mapped[str] = mapped_column(Text, ForeignKey("teams.id"), nullable=False)
    channelId: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    icon: Mapped[str] = mapped_column(Text, nullable=False)
    showDescription: Mapped[bool] = mapped_column(Boolean, nullable=False)
    isTemplate: Mapped[bool] = mapped_column(Boolean, nullable=False)
    templateVersion: Mapped[int] = mapped_column(Integer, nullable=False)
    minimumRole: Mapped[str] = mapped_column(Text, nullable=False)
    createAt: Mapped[int] = mapped_column(BigInteger, nullable=False)
    updateAt: Mapped[int] = mapped_column(BigInteger, nullable=False)
    deleteAt: Mapped[int] = mapped_column(BigInteger, nullable=False)

    team = relationship("Team", back_populates="boards")
    blocks = relationship("Block", back_populates="board")
    sharing = relationship("Sharing", uselist=False, back_populates="board")
    board_members = relationship("BoardMember", back_populates="board")
    board_categories = relationship("CategoryBoard", back_populates="board")
    limits = relationship("BoardLimits", uselist=False, back_populates="board")
    history = relationship("BoardHistory", back_populates="board")
    files = relationship("FileInfo", back_populates="board")


class BoardHistory(Base):
    __tablename__ = "board_history"

    id: Mapped[str] = mapped_column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    boardId: Mapped[str] = mapped_column(Text, ForeignKey("boards.id"), nullable=False)
    teamId: Mapped[str] = mapped_column(Text, nullable=False)
    channelId: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    icon: Mapped[str] = mapped_column(Text, nullable=False)
    showDescription: Mapped[bool] = mapped_column(Boolean, nullable=False)
    isTemplate: Mapped[bool] = mapped_column(Boolean, nullable=False)
    templateVersion: Mapped[int] = mapped_column(Integer, nullable=False)
    minimumRole: Mapped[str] = mapped_column(Text, nullable=False)
    createAt: Mapped[int] = mapped_column(BigInteger, nullable=False)
    updateAt: Mapped[int] = mapped_column(BigInteger, nullable=False)
    deleteAt: Mapped[int] = mapped_column(BigInteger, nullable=False)

    board = relationship("Board", back_populates="history")
