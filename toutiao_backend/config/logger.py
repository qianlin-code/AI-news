"""
统一日志配置
- 开发环境：控制台彩色输出 + 文件记录
- 生产环境：仅文件记录（ERROR 及以上发告警）
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

from config.settings import settings

# 日志格式
LOG_FORMAT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 日志目录
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)


def setup_logging() -> None:
    """初始化全局日志配置"""
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    # 清除已有的处理器（避免重复添加）
    root_logger.handlers.clear()

    # 1. 控制台输出（开发环境）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.WARNING)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT))
    root_logger.addHandler(console_handler)

    # 2. 文件输出（所有环境 — 按大小轮转，保留 7 天）
    file_handler = RotatingFileHandler(
        LOG_DIR / "app.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=7,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT))
    root_logger.addHandler(file_handler)

    # 3. 错误文件输出（ERROR 单独记录）
    error_handler = RotatingFileHandler(
        LOG_DIR / "error.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=7,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT))
    root_logger.addHandler(error_handler)

    # 降低第三方库的日志噪音
    logging.getLogger("aiomysql").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """获取模块专属日志器"""
    return logging.getLogger(name)
