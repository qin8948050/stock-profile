from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from core.config import config
from core.database import engine
from core.exceptions import http_exception_handler, generic_exception_handler, validation_exception_handler
from core.lifespan import lifespan
from core.middleware import register_middlewares
from routers import company, financial_statement

def create_app() -> FastAPI:
    """
    应用工厂函数，用于创建和配置 FastAPI 应用实例。
    """
    # -----------------------------
    # 1. 创建 FastAPI 应用实例
    # -----------------------------
    app = FastAPI(
        title=config.app.name,
        version=config.app.version,
        lifespan=lifespan
    )

    # -----------------------------
    # 2. 注册中间件
    # -----------------------------
    register_middlewares(app,engine)

    # -----------------------------
    # 3. 注册异常处理器
    # -----------------------------
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    # -----------------------------
    # 4. 注册路由
    # -----------------------------
    app.include_router(company.router, prefix=config.api.prefix)
    app.include_router(financial_statement.router, prefix=config.api.prefix)

    return app