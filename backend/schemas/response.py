from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from fastapi import status as http_status
from fastapi.encoders import jsonable_encoder

DataType = TypeVar('DataType')


class ApiResponse(BaseModel, Generic[DataType]):
    """
    通用 API 响应模型.
    提供了 success 和 error 类方法来快速创建标准响应.
    """
    status: int = Field(..., description="业务状态码, 200 表示成功")
    msg: str = Field(..., description="响应消息")
    data: Optional[DataType] = None

    @classmethod
    def success(cls, data: Optional[DataType] = None, msg: str = "success"):
        """
        创建并返回一个成功的 API JSON 响应.
        """
        content = {
            "status": 200,
            "msg": msg,
            "data": data
        }
        return JSONResponse(
            status_code=http_status.HTTP_200_OK,
            content=jsonable_encoder(content)
        )

    @classmethod
    def error(cls, msg: str, status: int = 400, http_code: int = http_status.HTTP_400_BAD_REQUEST):
        """
        创建并返回一个失败的 API JSON 响应.
        """
        content = {
            "status": status,
            "msg": msg,
            "data": None
        }
        return JSONResponse(
            status_code=http_code,
            content=jsonable_encoder(content)
        )
