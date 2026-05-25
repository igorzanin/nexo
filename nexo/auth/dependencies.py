import time

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from nexo.auth.jwt import decode_token
from nexo.db.session import get_db
from nexo.models import Session as SessionModel
from nexo.models import TeamMember, User

security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: DBSession = Depends(get_db),
) -> User:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    token = credentials.credentials
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    now = int(time.time() * 1000)
    sess = db.execute(
        select(SessionModel).where(SessionModel.token == token, SessionModel.expire_at > now)
    ).scalar_one_or_none()
    if sess is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired or revoked")
    user = db.query(User).filter(User.id == user_id, User.delete_at == 0).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


async def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: DBSession = Depends(get_db),
) -> User | None:
    if credentials is None:
        return None
    token = credentials.credentials
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    now = int(time.time() * 1000)
    sess = db.execute(
        select(SessionModel).where(SessionModel.token == token, SessionModel.expire_at > now)
    ).scalar_one_or_none()
    if sess is None:
        return None
    return db.query(User).filter(User.id == user_id, User.delete_at == 0).first()


async def require_admin(
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
) -> User:
    """Require that the current user is a scheme_admin in at least one team."""
    is_admin = db.execute(
        select(TeamMember).where(
            TeamMember.user_id == current_user.id,
            TeamMember.scheme_admin.is_(True),
            TeamMember.delete_at == 0,
        )
    ).scalar_one_or_none()
    if is_admin is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return current_user
