import uuid

from sqlalchemy import Text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship


from nexo.db.base import Base


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[str] = mapped_column(
        Text().with_variant(BigInteger, "sqlite").with_variant(Text, "postgresql").with_variant(Text, "mysql"),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    title: Mapped[str] = mapped_column(Text, nullable=False)
    signupToken: Mapped[str] = mapped_column(Text, nullable=False)
    modifiedBy: Mapped[str] = mapped_column(
        Text().with_variant(BigInteger, "sqlite").with_variant(Text, "postgresql").with_variant(Text, "mysql"),
        nullable=False,
    )
    updateAt: Mapped[int] = mapped_column(BigInteger, nullable=False)

    boards = relationship("Board", back_populates="team")
    categories = relationship("Category", back_populates="team")
