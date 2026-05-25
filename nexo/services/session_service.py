"""SessionService — BC-Identity.

Manages access-token–linked sessions for logout invalidation.
On login: create(). On logout: revoke(). On each request: is_active() (via dependencies.py).
"""
from __future__ import annotations

import time
from datetime import datetime, timedelta

from sqlalchemy.orm import Session as DBSession

from nexo.models import Session
from nexo.repositories.session import SessionRepository


class SessionService:
    def __init__(self, db: DBSession):
        self._repo = SessionRepository(db)

    def create(self, user_id: str, token: str, expire_days: int) -> Session:
        expire_at = int(
            (datetime.utcnow() + timedelta(days=expire_days)).timestamp() * 1000
        )
        return self._repo.create(user_id, token, expire_at)

    def is_active(self, token: str) -> bool:
        """Return True if the token has a non-expired session record."""
        session = self._repo.get_by_token(token)
        if not session:
            return False
        return session.expire_at > int(time.time() * 1000)

    def revoke(self, token: str) -> None:
        """Delete the session bound to this token (used on logout)."""
        session = self._repo.get_by_token(token)
        if session:
            self._repo.delete(session.id)

    def revoke_all_for_user(self, user_id: str) -> None:
        """Revoke all active sessions for a user (e.g., on password change)."""
        for session in self._repo.get_by_user(user_id):
            self._repo.delete(session.id)

    def cleanup_expired(self) -> int:
        """Purge expired sessions. Returns number of deleted records."""
        return self._repo.delete_expired()
