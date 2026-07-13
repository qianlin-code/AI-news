import json
from typing import Any

import redis.asyncio as redis

from config.logger import get_logger
from config.settings import settings

logger = get_logger("redis")

# 创建 Redis 的连接对象（配置从 .env 读取）
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,  # 将字节数据解码为字符串
    protocol=2,  # Redis 5.x 需要 RESP2 协议
)


async def get_json_cache(key: str) -> dict | list | None:
    """读取 JSON 缓存（字典或列表）"""
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        logger.error(f"获取 JSON 缓存失败 key={key}: {e}")
        return None


async def set_cache(key: str, value: Any, expire: int = 3600) -> bool:
    """设置缓存（字典/列表自动序列化为 JSON）"""
    try:
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        await redis_client.setex(key, expire, value)
        return True
    except Exception as e:
        logger.error(f"设置缓存失败 key={key}: {e}")
        return False
