from sqlalchemy import Text, Integer, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nexo.db.base import Base


class BoardLimits(Base):
    __tablename__ = "board_limits"

    boardId: Mapped[str] = mapped_column(Text, ForeignKey("boards.id"), primary_key=True)
    cards: Mapped[int] = mapped_column(Integer, nullable=False)
    usedCards: Mapped[int] = mapped_column(Integer, nullable=False)
    cardLimitTimestamp: Mapped[int] = mapped_column(BigInteger, nullable=False)
    views: Mapped[int] = mapped_column(Integer, nullable=False)

    board = relationship("Board", back_populates="limits")
