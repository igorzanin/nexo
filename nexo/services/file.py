import os
import uuid
from pathlib import Path

from fastapi import UploadFile


class FileService:
    def __init__(self, storage_path: str = "./storage/files"):
        self.storage_path = Path(storage_path)

    def store_file(self, board_id: str, file: UploadFile) -> tuple[str, str, int]:
        board_dir = self.storage_path / board_id
        board_dir.mkdir(parents=True, exist_ok=True)
        file_id = str(uuid.uuid4())
        ext = Path(file.filename).suffix if file.filename else ""
        dest = board_dir / f"{file_id}{ext}"
        content = file.file.read()
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
