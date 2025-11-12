import os
import time
from typing import Iterable, Optional
from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.trace import get_current_span
from core.log import logger


async def log_requests_and_add_trace_id(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000

    # 获取当前 trace_id
    span = get_current_span()
    trace_id = span.get_span_context().trace_id if span else None
    trace_id_hex = f"{trace_id:032x}" if trace_id else None

    if trace_id_hex:
        response.headers["X-Trace-Id"] = trace_id_hex

    logger.info(
        f'client="{request.client.host}:{request.client.port}" method="{request.method}" '
        f'path="{request.url.path}" status_code={response.status_code} time={process_time:.2f}ms '
        f'trace_id={trace_id_hex}'
    )
    return response


def _parse_allowed_origins(env_value: Optional[str]) -> Iterable[str]:
    if not env_value:
        return []
    env_value = env_value.strip()
    if env_value == "*":
        return ["*"]
    return [o.strip() for o in env_value.split(",") if o.strip()]


def register_middlewares(app: FastAPI) -> None:
    """Register application middlewares.

    This centralizes middleware registration (logging, CORS) so `main.py` stays small.
    Configure CORS via the `CORS_ALLOWED_ORIGINS` environment variable (comma-separated
    list) or leave unset to use sensible defaults for development.
    """
    # register request logging middleware
    app.middleware("http")(log_requests_and_add_trace_id)

    # Configure CORS
    # allowed_origins_env = os.getenv("CORS_ALLOWED_ORIGINS")
    # allowed_origins = list(_parse_allowed_origins(allowed_origins_env))
    # if not allowed_origins:
    #     allowed_origins = ['*']

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
