"""
全局配置管理
使用 pydantic-settings 从 .env 文件加载配置，所有硬编码值迁移到此处
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ========== 数据库 ==========
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "news_app"
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_ECHO: bool = False

    # ========== Redis ==========
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # ========== 应用 ==========
    APP_NAME: str = "新闻资讯API"
    DEBUG: bool = False
    CORS_ORIGINS: str = "http://127.0.0.1:5173"

    @property
    def database_url(self) -> str:
        """拼接异步数据库连接 URL"""
        return (
            f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
        )

    @property
    def cors_origin_list(self) -> list[str]:
        """解析逗号分隔的跨域来源列表"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()
