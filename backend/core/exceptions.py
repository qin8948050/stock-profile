from fastapi import Request,status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from core.log import logger
from schemas.response import ApiResponse


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    自定义 HTTPException, 使其返回统一的响应格式
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=ApiResponse(status=exc.status_code, msg=exc.detail, data=None).model_dump(),
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """
    通用异常处理器, 捕获所有未处理的异常
    """

    logger.error(f"未处理的异常: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ApiResponse(
            status=500, msg="Internal Server Error", data=None
        ).model_dump(),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    处理 Pydantic 验证错误 (RequestValidationError)，并将其封装到 ApiResponse 格式中。
    """
    error_messages = [f"{error['loc'][-1]}: {error['msg']}" for error in exc.errors()]
    detail_message = ", ".join(error_messages)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ApiResponse(
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            msg=f"Validation Error: {detail_message}",
        ).model_dump(exclude_none=True),
    )