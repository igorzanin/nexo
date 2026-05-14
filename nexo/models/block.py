import uuid

from sqlalchemy import Text, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.sqlite import JSON

from nexo.db.base import Base


class Block(Base):
    __tablename__ = "blocks"

    id: Mapped[str] = mapped_column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    boardId: Mapped[str] = mapped_column(Text, ForeignKey("boards.id"), nullable=False)
    parentId: Mapped[str] = mapped_column(Text, ForeignKey("blocks.id"), nullable=True)
    createdBy: Mapped[str] = mapped_column(Text, ForeignKey("users.id"), nullable=False)
    modifiedBy: Mapped[str] = mapped_column(Text, ForeignKey("users.id"), nullable=False)
    type: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    fields: Mapped[dict] = mapped_column(JSON, nullable=False)
    schema: Mapped[int] = mapped_column(Integer, nullable=False)
    createAt: Mapped[int] = mapped_column(BigInteger, nullable=False)
    updateAt: Mapped[int] = mapped_column(BigInteger, nullable=False)
    deleteAt: Mapped[int] = mapped_column(BigInteger, nullable=False)

    board = relationship("Board", back_populates="blocks")
    parent = relationship("Block", remote_side="Block.id", back_populates="children")
    children = relationship("Block", back_populates="parent")
    subscriptions = relationship("Subscription", back_populates="block")


class BlockHistory(Base):
    __tablename__ = "block_history"

    id: Mapped[str] = mapped_column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    blockId: Mapped[str] = mapped_column(Text, ForeignKey("blocks.id"), nullable=False)
    boardId: Mapped[str] = mapped_column(Text, ForeignKey("boards.id"), nullable=False)
    parentId: Mapped[str] = mapped_column(Text, nullable=False)
    createdBy: Mapped[str] = mapped_column(Text, nullable=False)
    modifiedBy: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    fields: Mapped[dict] = mapped_column(JSON, nullable=False)
    schema: Mapped[int] = mapped_column(Integer, nullable=False)
    createAt: Mapped[int] = mapped_column(BigInteger, nullable=False)
    updateAt: Mapped[int] = mapped_column(BigInteger, nullable=False)
    deleteAt: Mapped[int] = mapped_column(BigInteger, nullable=False)
