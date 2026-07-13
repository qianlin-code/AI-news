from datetime import datetime

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import News


async def add_history(db: AsyncSession, user_id: int, news_id: int) -> History:
    """添加浏览记录（去重+更新：已存在则刷新浏览时间）"""
    query = select(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(query)
    record = result.scalar_one_or_none()

    if record:
        record.view_time = datetime.now()
    else:
        record = History(user_id=user_id, news_id=news_id)
        db.add(record)

    await db.commit()
    await db.refresh(record)
    return record


async def get_list_history(
    db: AsyncSession,
    user_id: int,
    page: int,
    page_size: int,
) -> tuple[list[dict], int, bool]:
    """分页获取浏览历史，返回 (数据列表, 总条数, 是否还有更多)"""
    count_query = select(func.count(History.id)).where(History.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar()

    query = (
        select(News, History.view_time)
        .join(History, History.news_id == News.id)
        .where(History.user_id == user_id)
        .order_by(History.view_time.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(query)
    rows = result.all()

    has_more = (page * page_size) < total
    items = []
    for news, view_time in rows:
        items.append(
            {
                "id": news.id,
                "title": news.title,
                "description": news.description,
                "image": news.image,
                "author": news.author,
                "publishTime": news.publish_time,
                "categoryId": news.category_id,
                "views": news.views,
                "viewTime": view_time,
            }
        )
    return items, total, has_more


async def delete_history(db: AsyncSession, user_id: int, news_id: int) -> bool:
    """删除单条浏览记录"""
    stmt = delete(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


async def clear_history(db: AsyncSession, user_id: int) -> int:
    """清空用户所有浏览记录"""
    stmt = delete(History).where(History.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0
