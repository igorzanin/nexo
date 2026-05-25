import secrets
import time

from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from nexo.models import Sharing
from nexo.schemas.sharing import SharingCreate


class SharingRepository:
    def __init__(self, db: DBSession):
        self.db = db

    def get(self, board_id: str) -> Sharing | None:
        return self.db.get(Sharing, board_id)

    def get_by_token(self, token: str) -> Sharing | None:
        stmt = select(Sharing).where(Sharing.token == token, Sharing.enabled == True)
        return self.db.execute(stmt).scalar_one_or_none()

    def upsert(self, board_id: str, data: SharingCreate, modified_by: str | None = None) -> Sharing:
        now = int(time.time() * 1000)
        token = data.token if data.token else secrets.token_urlsafe(32)
        existing = self.get(board_id)
        if existing:
            existing.enabled = data.enabled
            existing.token = token
            existing.modified_by = modified_by
            existing.update_at = now
            self.db.commit()
            self.db.refresh(existing)
            return existing
        sharing = Sharing(
            id=board_id,
            enabled=data.enabled,
            token=token,
            modified_by=modified_by,
            create_at=now,
            update_at=now,
        )
        self.db.add(sharing)
        self.db.commit()
        self.db.refresh(sharing)
        return sharing

    def delete(self, board_id: str) -> bool:
        sharing = self.get(board_id)
        if not sharing:
            return False
        self.db.delete(sharing)
        self.db.commit()
        return True
