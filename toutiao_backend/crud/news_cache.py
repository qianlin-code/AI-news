"""新闻相关缓存业务逻辑 — 在纯 DB 操作之上叠加 Redis 缓存层"""
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from models.news import News
from crud.news import (  # 导入基础 DB 操作，不重复定义
    get_categories as _db_get_categories,
    get_news_list as _db_get_news_list,
    get_news_detail as _db_get_news_detail,
    get_related_news as _db_get_related_news,
)
from cache.news_cache import (
    get_cache_categories, set_cache_categories,
    get_cache_news_list, set_cache_news_list,
    get_cache_news_detail, set_cache_news_detail,
    get_cache_related_news, set_cache_related_news,
)
from schemas.base import NewsItemBase, NewsDetailItem


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    """获取分类列表（优先读缓存）"""
    cached = await get_cache_categories()
    if cached:
        return cached

    categories = await _db_get_categories(db, skip, limit)
    if categories:
        await set_cache_categories(jsonable_encoder(categories))
    return categories


async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    """获取新闻列表（优先读缓存）"""
    page = skip // limit + 1
    cached = await get_cache_news_list(category_id, page, limit)
    if cached:
        return [News(**item) for item in cached]

    news_list = await _db_get_news_list(db, category_id, skip, limit)
    if news_list:
        news_data = [
            NewsItemBase.model_validate(item).model_dump(mode="json", by_alias=False)
            for item in news_list
        ]
        await set_cache_news_list(category_id, page, limit, news_data)
    return news_list


async def get_news_detail_cached(db: AsyncSession, news_id: int) -> dict | None:
    """获取新闻详情（优先读缓存）"""
    cached = await get_cache_news_detail(news_id)
    if cached:
        return cached

    news_detail = await _db_get_news_detail(db, news_id)
    if not news_detail:
        return None

    detail_dict = NewsDetailItem.model_validate(news_detail).model_dump(
        mode="json", by_alias=False
    )
    await set_cache_news_detail(news_id, detail_dict)
    return detail_dict


async def get_related_news_cached(db: AsyncSession, news_id: int, category_id: int, limit: int = 5) -> list[dict]:
    """获取相关新闻推荐（优先读缓存）"""
    cached = await get_cache_related_news(news_id)
    if cached:
        return cached

    related = await _db_get_related_news(db, news_id, category_id, limit)
    if related:
        await set_cache_related_news(news_id, related)
    return related
