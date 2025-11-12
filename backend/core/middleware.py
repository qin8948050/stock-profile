import time
from fastapi import Request
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
