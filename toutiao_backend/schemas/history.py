from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


# 添加浏览历史——请求体
class HistoryAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId", description="新闻ID")


# 添加浏览历史——响应 data
class HistoryResponse(BaseModel):
    id: int
    user_id: int = Field(..., alias="userId")
    news_id: int = Field(..., alias="newsId")
    view_time: datetime = Field(..., alias="viewTime")

    model_config = ConfigDict(
        from_attributes=True,  # 允许从 ORM 对象取值
        populate_by_name=True  # 兼容 alias 和字段名
    )


# 获取浏览历史列表
class HistoryListItem(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    publish_time: datetime = Field(..., alias="publishTime")
    category_id: int = Field(..., alias="categoryId")
    views: int
    view_time: datetime = Field(..., alias="viewTime")

    model_config = ConfigDict(populate_by_name=True)


class HistoryListData(BaseModel):
    list: list[HistoryListItem]
    total: int
    has_more: bool = Field(..., alias="hasMore")

    model_config = ConfigDict(populate_by_name=True)
