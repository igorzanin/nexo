# Servidor Web — obsoleto

## Design

O antigo `server/web/webserver.go` (gorilla/mux + http.FileServer) é substituído pela configuração direta do FastAPI + Uvicorn.

### Configuração

```python
# settings.py
class Settings(BaseSettings):
    # Server
    server_root: str = "http://localhost:8000"
    port: int = 8000
    ssl: bool = False
    local_only: bool = False
    ssl_certfile: str = ""
    ssl_keyfile: str = ""
    server_basepath: str = Field("", alias="FOCALBOARD_HTTP_SERVER_BASEPATH")

    # Security
    read_header_timeout: int = 10  # segundos
    rate_limit_enabled: bool = True

    # Auth
    secret_key: str
    access_token_expire_days: int = 30
```

```python
# main.py
def create_app() -> FastAPI:
    app = FastAPI(title="Nexo", version="2.0.0")

    app.add_middleware(TrustedHostMiddleware, ...)

    # Static files
    webapp_dir = Path(__file__).parent.parent / "webapp" / "dist"
    if webapp_dir.exists():
        app.mount("/static", StaticFiles(directory=str(webapp_dir / "static")), name="static")

        @app.get("/{full_path:path}")
        async def catch_all(full_path: str):
            return FileResponse(str(webapp_dir / "index.html"))
    else:
        # Dev mode — Vite proxy
        pass

    # Routers
    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(boards_router, prefix="/api/v1")
    # ...

    return app
```

## Tarefa única

- [ ] T-01, Configurar FastAPI para servir arquivos estáticos + catch-all SPA
  - Fonte legado: `server/web/webserver.go`
  - Critério: Static files servidos em `/static/*`; catch-all retorna index.html
