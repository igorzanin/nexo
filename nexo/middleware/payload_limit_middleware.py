"""BR-MIGRAR-024 — Limite de payload do body (proteção contra DoS).

Retorna 413 se o Content-Length declarado (ou corpo lido) exceder
MAX_PAYLOAD_SIZE (configurável via env; padrão 10 MB).

Exceção: uploads de arquivo são tratados pelo endpoint /files/ com limite
próprio de 100 KB (max_file_size no Settings), então não passamos por aqui
com um limite menor.
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class PayloadLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_bytes: int = 10 * 1024 * 1024):
        super().__init__(app)
        self.max_bytes = max_bytes

    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_bytes:
            return JSONResponse(
                {"detail": f"Payload too large. Maximum allowed: {self.max_bytes} bytes."},
                status_code=413,
            )
        return await call_next(request)
