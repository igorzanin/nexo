"""BR-MIGRAR-020 — Prometheus metrics middleware.

Instrumenta cada request HTTP com:
  - nexo_http_requests_total{method, path, status}  (Counter)
  - nexo_http_request_duration_seconds{method, path} (Histogram)

O endpoint /metrics é montado em main.py via make_asgi_app().
"""
import time

from prometheus_client import Counter, Histogram
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

REQUEST_COUNT = Counter(
    "nexo_http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"],
)

REQUEST_DURATION = Histogram(
    "nexo_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "path"],
)


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        method = request.method
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start

        REQUEST_COUNT.labels(method=method, path=path, status=str(response.status_code)).inc()
        REQUEST_DURATION.labels(method=method, path=path).observe(duration)
        return response
