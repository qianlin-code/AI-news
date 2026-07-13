"""新闻缓存 Key 管理 — 定义 Key 命名规范和读写函数"""

from typing import Any

from config.cache_conf import get_json_cache, set_cache

CATEGORIES_KEY = "news:categories"
NEWS_LIST_PREFIX = "news:list:"
NEWS_DETAIL_PREFIX = "news:detail:"
RELATED_NEWS_PREFIX = "news:related:"


async def get_cache_categories() -> list[dict] | None:
    """读取分类缓存"""
    return await get_json_cache(CATEGORIES_KEY)


async def set_cache_categories(data: list[dict[str, Any]], expire: int = 7200) -> bool:
    """写入分类缓存（默认 2 小时）"""
    return await set_cache(CATEGORIES_KEY, data, expire)


async def get_cache_news_list(category_id: int | None, page: int, size: int) -> list[dict] | None:
    """读取新闻列表缓存"""
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"
    return await get_json_cache(key)


async def set_cache_news_list(
    category_id: int | None, page: int, size: int, news_list: list[dict], expire: int = 1800
) -> bool:
    """写入新闻列表缓存（默认 30 分钟）"""
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"
    return await set_cache(key, news_list, expire)


async def get_cache_news_detail(news_id: int) -> dict | None:
    """读取新闻详情缓存"""
    key = f"{NEWS_DETAIL_PREFIX}{news_id}"
    return await get_json_cache(key)


async def set_cache_news_detail(news_id: int, detail: dict, expire: int = 1800) -> bool:
    """写入新闻详情缓存（默认 30 分钟）"""
    key = f"{NEWS_DETAIL_PREFIX}{news_id}"
    return await set_cache(key, detail, expire)


async def get_cache_related_news(news_id: int) -> list[dict] | None:
    """读取相关推荐缓存"""
    key = f"{RELATED_NEWS_PREFIX}{news_id}"
    return await get_json_cache(key)


async def set_cache_related_news(news_id: int, data: list[dict], expire: int = 120) -> bool:
    """写入相关推荐缓存（默认 2 分钟，推荐数据变化快）"""
    key = f"{RELATED_NEWS_PREFIX}{news_id}"
    return await set_cache(key, data, expire)
