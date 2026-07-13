from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from config.settings import settings

# 创建异步数据库引擎（配置从 .env 读取）
async_engine = create_async_engine(
    settings.database_url,
    echo=settings.DB_ECHO,  # 打印执行的SQL日志，开发调试打开，生产关闭
    pool_size=settings.DB_POOL_SIZE,  # 连接池常驻连接数量
    max_overflow=settings.DB_MAX_OVERFLOW  # 高峰期额外临时最大连接
)

# 异步会话工厂：批量生成数据库会话对象
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False  # commit后不失效对象，查询后可继续使用模型实例
)


# FastAPI 标准数据库依赖项（获取会话）
async def get_db():
    # 自动创建会话，结束自动关闭
    async with AsyncSessionLocal() as session:
        try:
            yield session  # 把会话交给接口业务逻辑使用
            await session.commit()  # 业务无异常则提交事务
        except Exception as e:
            await session.rollback()  # 出现异常回滚事务，防止脏数据
            raise e  # 抛出异常交给上层捕获处理
        finally:
            await session.close()  # 无论成功失败，最终关闭会话归还连接池
