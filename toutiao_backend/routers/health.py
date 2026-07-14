"""
健康检查接口 —— 供 Docker / K8s 探活使用

GET /health 返回服务状态和各依赖组件的连通性检测结果
"""

import time

from fastapi import APIRouter

from utils.response import success_response

router = APIRouter(tags=["health"])

# 记录服务启动时间（用于计算 uptime）
START_TIME = time.time()


@router.get("/health")
async def health_check():
    """健康检查：返回服务状态和各依赖组件连通性"""
    health_data = {
        "status": "ok",
        "service": "AI掘金头条",
        "uptime_seconds": round(time.time() - START_TIME, 1),
        "checks": {
            "api": "ok",
            # 数据库和Redis的连通性后面会补充
        },
    }
    return success_response(message="服务运行正常", data=health_data)
