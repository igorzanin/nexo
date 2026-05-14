from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from nexo.routers.auth import router as auth_router, limiter
from nexo.routers.ws import router as ws_router
from nexo.routers.boards import router as boards_router
from nexo.routers.blocks import router as blocks_router
from nexo.routers.cards import router as cards_router
from nexo.routers.categories import router as categories_router
from nexo.routers.members import router as members_router
from nexo.routers.files import router as files_router
from nexo.routers.teams import router as teams_router
from nexo.routers.admin import router as admin_router
from nexo.routers.subscriptions import router as subscriptions_router
from nexo.routers.sharing import router as sharing_router

app = FastAPI(title="Nexo", version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth_router)
app.include_router(ws_router)
app.include_router(boards_router)
app.include_router(blocks_router)
app.include_router(cards_router)
app.include_router(categories_router)
app.include_router(members_router)
app.include_router(files_router)
app.include_router(teams_router)
app.include_router(admin_router)
app.include_router(subscriptions_router)
app.include_router(sharing_router)

webapp_dir = Path(__file__).resolve().parent.parent / "webapp" / "dist"
static_dir = webapp_dir if webapp_dir.exists() else None

if static_dir:
    app.mount("/static", StaticFiles(directory=str(static_dir / "static")), name="static")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api/") or full_path.startswith("ws"):
            from fastapi.responses import JSONResponse
            return JSONResponse({"detail": "Not Found"}, status_code=404)
        index = static_dir / "index.html"
        if index.exists():
            return FileResponse(str(index))
        return JSONResponse({"detail": "Not Found"}, status_code=404)
