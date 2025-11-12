from pathlib import Path
from fastapi import FastAPI
import uvicorn
from starlette.exceptions import HTTPException as StarletteHTTPException

from routers import company
from core.log import init_log
from core.config import config
from core.exceptions import http_exception_handler, generic_exception_handler
from core.middleware import log_requests_and_add_trace_id
from core.lifespan import lifespan

init_log(log_level=config.logging.level,log_file=Path(config.logging.file))

# -----------------------------
# 创建 FastAPI 应用
# -----------------------------
app = FastAPI(
    title=config.app.name,
    version=config.app.version,
    lifespan=lifespan
)

# -----------------------------
# 注册中间件
# -----------------------------
app.middleware("http")(log_requests_and_add_trace_id)

# -----------------------------
# 注册异常处理器
# -----------------------------
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# -----------------------------
# 注册路由
# -----------------------------
app.include_router(company.router,prefix=config.api.prefix)

# -----------------------------
# 启动入口（支持直接运行）
# -----------------------------
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.server.host,
        port=config.app.port,
        reload=config.server.reload,
        log_level=config.server.log_level.lower(),
        access_log=False  # 禁用 uvicorn 默认的访问日志
    )