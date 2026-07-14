from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.middleware.cors import CORSMiddleware

from config.db_conf import AsyncSessionLocal
from config.logger import get_logger, setup_logging
from config.settings import settings
from middleware.logging import RequestLoggingMiddleware
from routers import favorite, health, history, news, users
from utils.exception_handlers import register_exception_handlers

# 初始化日志系统
setup_logging()
logger = get_logger("app")


async def warmup_cache():
    """启动时预热缓存：把分类和首页新闻列表提前加载到 Redis"""
    try:
        from fastapi.encoders import jsonable_encoder

        from cache.news_cache import set_cache_categories, set_cache_news_list
        from crud.news import get_categories as db_get_categories
        from crud.news import get_news_list as db_get_news_list
        from schemas.base import NewsItemBase

        async with AsyncSessionLocal() as db:
            # 预热分类
            categories = await db_get_categories(db)
            if categories:
                await set_cache_categories(jsonable_encoder(categories))
                logger.info(f"缓存预热: 分类 {len(categories)} 条")

            # 预热前 3 个分类的首页新闻列表
            category_ids = [c.id for c in categories[:3]] if categories else []
            for cid in category_ids:
                news = await db_get_news_list(db, cid, skip=0, limit=10)
                if news:
                    data = [
                        NewsItemBase.model_validate(n).model_dump(mode="json", by_alias=False) for n in news
                    ]
                    await set_cache_news_list(cid, page=1, size=10, news_list=data)
            logger.info(f"缓存预热: 新闻列表 {len(category_ids)} 个分类")

    except Exception as e:
        logger.warning(f"缓存预热失败（不影响正常使用）: {e}")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """应用生命周期：启动时预热缓存"""
    logger.info(f"应用启动: {settings.APP_NAME}, DEBUG={settings.DEBUG}")
    await warmup_cache()
    yield  # 应用运行中...
    logger.info("应用关闭")


app = FastAPI(
    title=settings.APP_NAME,
    docs_url=None,  # 禁用默认 Swagger，使用自定义 CDN 版
    lifespan=lifespan,
)

# 注册全局异常处理器
register_exception_handlers(app)

# 件请求日志中间（需在 CORS 之前）
app.add_middleware(RequestLoggingMiddleware)

# CORS 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,  # 从 .env 读取，不允许 "*" + credentials 同时用
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Swagger UI（使用国内 CDN，加载更快）
SWAGGER_JS = "https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.17.14/swagger-ui-bundle.js"
SWAGGER_CSS = "https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.17.14/swagger-ui.min.css"


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_js_url=SWAGGER_JS,
        swagger_css_url=SWAGGER_CSS,
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 注册路由
app.include_router(health.router)
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)
