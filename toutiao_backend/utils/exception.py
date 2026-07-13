"""
全局异常处理器
- 开发模式：返回详细错误信息（堆栈、路径）
- 生产模式：返回简化信息，不泄露内部细节
"""

import traceback

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette import status

from config.logger import get_logger
from config.settings import settings

logger = get_logger("exception")


async def http_exception_handler(request: Request, exc: HTTPException):
    """处理业务层主动抛出的 HTTP 异常"""
    logger.warning(f"HTTP异常 {exc.status_code}: {exc.detail} | {request.method} {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data": None,
        },
    )


async def validation_error_handler(request: Request, exc: RequestValidationError):
    """处理请求参数校验失败（Pydantic 验证错误）"""
    # 提取第一个校验错误信息，返回友好提示
    errors = exc.errors()
    detail = errors[0].get("msg", "参数校验失败") if errors else "参数校验失败"
    logger.warning(f"参数校验失败: {detail} | {request.method} {request.url.path}")

    error_data = None
    if settings.DEBUG:
        error_data = {
            "error_type": "RequestValidationError",
            "errors": errors,
            "path": str(request.url),
        }

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "code": 422,
            "message": detail,
            "data": error_data,
        },
    )


async def integrity_error_handler(request: Request, exc: IntegrityError):
    """处理数据库完整性约束错误（唯一键冲突、外键不存在等）"""
    error_msg = str(exc.orig)

    if "username_UNIQUE" in error_msg or "Duplicate entry" in error_msg:
        detail = "用户名已存在"
    elif "FOREIGN KEY" in error_msg:
        detail = "关联数据不存在"
    else:
        detail = "数据约束冲突，请检查输入"

    logger.warning(f"数据完整性错误: {detail} | {request.method} {request.url.path}")

    error_data = None
    if settings.DEBUG:
        error_data = {
            "error_type": "IntegrityError",
            "error_detail": error_msg,
            "path": str(request.url),
        }

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": 400,
            "message": detail,
            "data": error_data,
        },
    )


async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """处理 SQLAlchemy 数据库错误"""
    logger.error(f"数据库错误: {exc} | {request.method} {request.url.path}", exc_info=True)

    error_data = None
    if settings.DEBUG:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            "traceback": traceback.format_exc(),
            "path": str(request.url),
        }

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "数据库操作失败，请稍后重试",
            "data": error_data,
        },
    )


async def general_exception_handler(request: Request, exc: Exception):
    """兜底处理器：捕获所有未处理的异常"""
    logger.error(
        f"未处理异常 {type(exc).__name__}: {exc} | {request.method} {request.url.path}",
        exc_info=True,
    )

    error_data = None
    if settings.DEBUG:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            "traceback": traceback.format_exc(),
            "path": str(request.url),
        }

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "data": error_data,
        },
    )
