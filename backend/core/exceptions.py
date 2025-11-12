from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from core.log import logger

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    自定义 HTTPException, 使其返回统一的响应格式
    """
    from schemas.response import ApiResponse
    return JSONResponse(
        status_code=exc.status_code,
        content=ApiResponse(status=exc.status_code, msg=exc.detail, data=None).model_dump(),
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """
    通用异常处理器, 捕获所有未处理的异常
    """
    from schemas.response import ApiResponse
    logger.error(f"未处理的异常: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ApiResponse(
            status=500, msg="Internal Server Error", data=None
        ).model_dump(),
    )
