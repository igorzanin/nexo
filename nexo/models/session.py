import uuid

from sqlalchemy import Text, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nexo.db.base import Base


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    token: Mapped[str] = mapped_column(Text, nullable=False)
    userId: Mapped[str] = mapped_column(Text, ForeignKey("users.id"), nullable=False)
    createAt: Mapped[int] = mapped_column(BigInteger, nullable=False)
    updateAt: Mapped[int] = mapped_column(BigInteger, nullable=False)
    expiresAt: Mapped[int] = mapped_column(BigInteger, nullable=False)

    user = relationship("User", back_populates="sessions")
