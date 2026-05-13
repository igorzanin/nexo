# Autenticação, Design Técnico

## Estrutura

```
nexo/
├── auth/
│   ├── __init__.py
│   ├── jwt.py           # create_access_token, create_refresh_token, decode_token
│   ├── password.py      # hash_password, verify_password
│   ├── dependencies.py  # get_current_user, get_optional_user
│   └── schemas.py       # LoginRequest, TokenResponse, RegisterRequest, etc.
└── routers/
    └── auth.py           # FastAPI router com endpoints
```

## JWT Tokens

```python
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30
REFRESH_TOKEN_EXPIRE_DAYS = 60

def create_access_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(401, "Invalid token")
```

## Password Hashing

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

## Auth Dependency

```python
# dependencies.py
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    payload = decode_token(token)
    if payload.get("type") != "access":
        raise HTTPException(401)
    user = user_repo.get(db, payload["sub"])
    if not user:
        raise HTTPException(404)
    return user
```

## Fluxo de Login

1. Cliente envia POST `/api/v1/login` com username + password
2. Rate limiter verifica quota do IP
3. Busca usuário por username ou email no banco
4. Compara hash bcrypt da senha
5. Gera access_token (30 dias) + refresh_token (60 dias)
6. Incrementa métrica de login sucesso/falha
7. Retorna tokens

## Dependências Python
- `python-jose[cryptography]`
- `passlib[bcrypt]`
- `slowapi`
