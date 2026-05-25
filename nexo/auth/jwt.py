from datetime import datetime, timedelta
from uuid import uuid4

from jose import JWTError, jwt

from nexo.config import get_settings

settings = get_settings()


def create_access_token(sub: str) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.access_token_expire_days)
    payload = {"sub": sub, "exp": expire, "type": "access", "jti": str(uuid4())}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def create_refresh_token(sub: str) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    payload = {"sub": sub, "exp": expire, "type": "refresh", "jti": str(uuid4())}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        return {}
