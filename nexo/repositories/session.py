import time

from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from nexo.models import Session


class SessionRepository:
    def __init__(self, db: DBSession):
        self.db = db

    def get(self, session_id: str) -> Session | None:
        return self.db.get(Session, session_id)

    def get_by_token(self, token: str) -> Session | None:
        stmt = select(Session).where(Session.token == token)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_user(self, user_id: str) -> list[Session]:
        stmt = select(Session).where(Session.user_id == user_id)
        return list(self.db.execute(stmt).scalars().all())

    def create(self, user_id: str, token: str, expires_at: int) -> Session:
        now = int(time.time() * 1000)
        session = Session(
            token=token,
            user_id=user_id,
            create_at=now,
            last_active_time=now,
            expire_at=expires_at,
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def delete(self, session_id: str) -> bool:
        session = self.get(session_id)
        if not session:
            return False
        self.db.delete(session)
        self.db.commit()
        return True

    def delete_expired(self) -> int:
        now = int(time.time() * 1000)
        stmt = select(Session).where(Session.expire_at < now)
        expired = list(self.db.execute(stmt).scalars().all())
        for s in expired:
            self.db.delete(s)
        self.db.commit()
        return len(expired)
