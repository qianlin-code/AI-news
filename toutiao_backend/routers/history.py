from fastapi import APIRouter, Query
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from models.users import User
from schemas.history import HistoryAddRequest, HistoryResponse
from utils.auth import get_current_user
from utils.response import success_response
from crud import history as history_crud

router = APIRouter(prefix="/api/history", tags=["history"])


@router.post("/add")
async def add_history(
        history_data: HistoryAddRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    record = await history_crud.add_history(db, user.id, history_data.news_id)
    return success_response(message="添加成功", data=HistoryResponse.model_validate(record))


@router.get("/list")
async def get_history_list(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    items, total, has_more = await history_crud.get_list_history(db, user.id, page, page_size)
    return success_response(message="success", data={"list": items, "total": total, "hasMore": has_more})


@router.delete("/delete/{history_id}")
async def delete_history(
        history_id: int,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await history_crud.delete_history(db, user.id, history_id)
    return success_response(message="删除成功", data=result)


@router.delete("/clear")
async def clear_history(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    count = await history_crud.clear_history(db, user.id)
    return success_response(message=f"清空了{count}条记录")
