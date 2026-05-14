from sqlalchemy import Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nexo.db.base import Base


class Sharing(Base):
    __tablename__ = "sharings"

    id: Mapped[str] = mapped_column(Text, ForeignKey("boards.id"), primary_key=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False)
    token: Mapped[str] = mapped_column(Text, nullable=False)

    board = relationship("Board", back_populates="sharing")
