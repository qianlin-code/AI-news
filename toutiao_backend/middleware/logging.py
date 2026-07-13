"""
请求日志中间件
记录每个 HTTP 请求的方法、路径、状态码、耗时
"""

import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("request")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # 执行下游（路由 → 业务逻辑）
        response = await call_next(request)

        # 计算耗时
        duration_ms = (time.time() - start_time) * 1000

        # 日志格式：GET /api/news/detail?id=1 → 200 (42.3ms)
        logger.info(
            "%s %s → %s (%.1fms)",
            request.method,
            request.url.path + ("?" + request.url.query if request.url.query else ""),
            response.status_code,
            duration_ms,
        )

        return response
