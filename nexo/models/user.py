import uuid

from sqlalchemy import Text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nexo.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    username: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    createAt: Mapped[int] = mapped_column(BigInteger, nullable=False)
    updateAt: Mapped[int] = mapped_column(BigInteger, nullable=False)
    deleteAt: Mapped[int] = mapped_column(BigInteger, nullable=False)

    sessions = relationship("Session", back_populates="user")
    board_memberships = relationship("BoardMember", back_populates="user")
    categories = relationship("Category", back_populates="user")
