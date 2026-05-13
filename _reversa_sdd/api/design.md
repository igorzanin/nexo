# API, Design Técnico

## Estrutura de Pacotes

```
nexo/routers/
├── __init__.py
├── auth.py         # login, register, logout, change_password
├── boards.py       # CRUD boards + duplicate
├── blocks.py       # CRUD blocks + batch insert
├── cards.py        # CRUD cards
├── categories.py   # CRUD categories + reorder
├── members.py      # CRUD board members
├── files.py        # upload/download
├── teams.py        # team CRUD
├── admin.py        # admin config
├── subscriptions.py # subscription CRUD
└── sharing.py      # sharing public token
main.py              # FastAPI app creation
dependencies.py      # auth dependency, rate limiter
```

## FastAPI App

```python
app = FastAPI(title="Nexo API", version="2.0.0")

app.add_middleware(RateLimitMiddleware)
app.add_middleware(TrustedHostMiddleware)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(boards_router, prefix="/api/v1")
app.include_router(blocks_router, prefix="/api/v1/boards/{board_id}")
# ...

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
```

## Autenticação JWT

```python
# dependencies.py
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user = user_repo.get(db, payload["sub"])
    if not user:
        raise HTTPException(403)
    return user

# Uso nos routers
@router.post("/api/v1/boards")
async def create_board(
    data: BoardCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return board_service.create(db, data, user)
```

## Fluxo Principal

1. Requisição chega ao FastAPI router
2. Dependency injection valida JWT (exceto login/register)
3. Pydantic schema valida body da requisição
4. Router chama service layer
5. Service layer aplica regras de negócio + chama repositories
6. Resposta Pydantic serializada como JSON

## Rate Limiting

```python
@router.post("/api/v1/login")
@limiter.limit("10/minute")
async def login(request: Request, data: LoginRequest, db: Session = Depends(get_db)):
    ...
```

## Dependências Python
- `fastapi`, `uvicorn[standard]`
- `python-jose[cryptography]` (JWT)
- `passlib[bcrypt]` (password hashing)
- `python-multipart` (file upload)
- `slowapi` (rate limiting)
- `prometheus-client` (metrics)
