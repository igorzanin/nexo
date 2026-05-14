from sqlalchemy import Text, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nexo.db.base import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    blockId: Mapped[str] = mapped_column(Text, ForeignKey("blocks.id"), primary_key=True)
    subscriberId: Mapped[str] = mapped_column(Text, primary_key=True)
    subscriberType: Mapped[str] = mapped_column(Text, nullable=False)
    createAt: Mapped[int] = mapped_column(BigInteger, nullable=False)
    notifyAt: Mapped[int] = mapped_column(BigInteger, nullable=False)
    updateAt: Mapped[int] = mapped_column(BigInteger, nullable=False)

    block = relationship("Block", back_populates="subscriptions")
