import uuid

import uuid

from sqlalchemy import Text, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nexo.db.base import Base


class FileInfo(Base):
    __tablename__ = "file_infos"

    id: Mapped[str] = mapped_column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    boardId: Mapped[str] = mapped_column(Text, ForeignKey("boards.id"), nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    extension: Mapped[str] = mapped_column(Text, nullable=False)
    size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    mimeType: Mapped[str] = mapped_column(Text, nullable=False)
    path: Mapped[str] = mapped_column(Text, nullable=False)
    createAt: Mapped[int] = mapped_column(BigInteger, nullable=False)
    deleteAt: Mapped[int] = mapped_column(BigInteger, nullable=False)

    board = relationship("Board", back_populates="files")
