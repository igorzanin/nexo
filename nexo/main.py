import logging
import logging.config
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from prometheus_client import make_asgi_app
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from nexo.config import get_settings
from nexo.middleware.logging_middleware import LoggingMiddleware
from nexo.middleware.metrics_middleware import MetricsMiddleware
from nexo.middleware.payload_limit_middleware import PayloadLimitMiddleware
from nexo.routers.auth import router as auth_router, limiter
from nexo.routers.users import router as users_router
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
from nexo.routers.views import router as views_router

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {"format": "%(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        }
    },
    "root": {"handlers": ["console"], "level": "INFO"},
})


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    settings = get_settings()

    application = FastAPI(
        title="Nexo",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Rate limiter
    application.state.limiter = limiter
    application.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Payload limit (BR-MIGRAR-024)
    application.add_middleware(PayloadLimitMiddleware, max_bytes=settings.max_payload_size)

    # Prometheus metrics (BR-MIGRAR-020)
    application.add_middleware(MetricsMiddleware)

    # Structured JSON access log (BR-MIGRAR-023)
    application.add_middleware(LoggingMiddleware)

    # Routers
    application.include_router(auth_router)
    application.include_router(users_router)
    application.include_router(ws_router)
    application.include_router(boards_router)
    application.include_router(blocks_router)
    application.include_router(cards_router)
    application.include_router(categories_router)
    application.include_router(members_router)
    application.include_router(files_router)
    application.include_router(teams_router)
    application.include_router(admin_router)
    application.include_router(subscriptions_router)
    application.include_router(sharing_router)
    application.include_router(views_router)

    # /health
    @application.get("/health", tags=["ops"])
    async def health():
        return {"status": "ok"}

    # /metrics (Prometheus)
    metrics_app = make_asgi_app()
    application.mount("/metrics", metrics_app)

    # SPA static files (optional — only when webapp/dist exists)
    webapp_dir = Path(__file__).resolve().parent.parent / "webapp" / "dist"
    if webapp_dir.exists():
        application.mount("/assets", StaticFiles(directory=str(webapp_dir / "assets")), name="assets")

        @application.get("/{full_path:path}")
        async def serve_spa(full_path: str):
            if full_path.startswith("api/") or full_path.startswith("ws"):
                return JSONResponse({"detail": "Not Found"}, status_code=404)
            index = webapp_dir / "index.html"
            if index.exists():
                return FileResponse(str(index))
            return JSONResponse({"detail": "Not Found"}, status_code=404)

    return application


app = create_app()

