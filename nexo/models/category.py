import uuid

from sqlalchemy import Text, BigInteger, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nexo.db.base import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(Text, nullable=False)
    userID: Mapped[str] = mapped_column(Text, ForeignKey("users.id"), nullable=False)
    teamID: Mapped[str] = mapped_column(Text, ForeignKey("teams.id"), nullable=False)
    type: Mapped[str] = mapped_column(Text, nullable=False)
    collapsed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    sortOrder: Mapped[int] = mapped_column(Integer, nullable=False)
    createAt: Mapped[int] = mapped_column(BigInteger, nullable=False)
    updateAt: Mapped[int] = mapped_column(BigInteger, nullable=False)
    deleteAt: Mapped[int] = mapped_column(BigInteger, nullable=False)

    user = relationship("User", back_populates="categories")
    team = relationship("Team", back_populates="categories")
    board_categories = relationship("CategoryBoard", back_populates="category")


class CategoryBoard(Base):
    __tablename__ = "category_boards"

    categoryId: Mapped[str] = mapped_column(Text, ForeignKey("categories.id"), primary_key=True)
    boardId: Mapped[str] = mapped_column(Text, ForeignKey("boards.id"), primary_key=True)
    sortOrder: Mapped[int] = mapped_column(Integer, nullable=False)
    hidden: Mapped[bool] = mapped_column(Boolean, nullable=False)

    category = relationship("Category", back_populates="board_categories")
    board = relationship("Board", back_populates="board_categories")
