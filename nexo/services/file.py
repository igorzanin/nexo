import time
import uuid
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session as DBSession

from nexo.models.fileinfo import FileInfo


class FileService:
    def __init__(self, storage_path: str = "./storage/files"):
        self.storage_path = Path(storage_path)

    def store_file(self, board_id: str, file: UploadFile, content: bytes) -> tuple[str, str, int]:
        """Store file bytes to disk. Content already read by caller."""
        board_dir = self.storage_path / board_id
        board_dir.mkdir(parents=True, exist_ok=True)
        file_id = str(uuid.uuid4())
        ext = Path(file.filename).suffix if file.filename else ""
        dest = board_dir / f"{file_id}{ext}"
        dest.write_bytes(content)
        return file_id, ext, len(content)

    def read_file(self, board_id: str, file_id: str, ext: str = "") -> bytes | None:
        path = self.storage_path / board_id / f"{file_id}{ext}"
        if not path.exists():
            return None
        return path.read_bytes()

    def remove_file(self, board_id: str, file_id: str, ext: str = "") -> bool:
        path = self.storage_path / board_id / f"{file_id}{ext}"
        if not path.exists():
            return False
        path.unlink()
        return True

    def persist_metadata(
        self,
        db: DBSession,
        file_id: str,
        board_id: str,
        creator_id: str,
        name: str,
        extension: str,
        size: int,
        mime_type: str | None = None,
    ) -> FileInfo:
        now = int(time.time() * 1000)
        record = FileInfo(
            id=file_id,
            creator_id=creator_id,
            board_id=board_id,
            create_at=now,
            update_at=now,
            delete_at=0,
            path=f"{board_id}/{file_id}{extension}",
            name=name,
            extension=extension,
            size=size,
            mime_type=mime_type,
            has_preview_image=False,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
