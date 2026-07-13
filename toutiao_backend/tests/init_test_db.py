"""
CI 测试数据库初始化 —— 创建表结构 + 种子数据

在 GitHub Actions 中，MySQL 服务容器是全新空白的，需要：
  1. 创建所有表
  2. 插入测试用的分类和新闻数据

本地不需要运行这个脚本（你已经有数据库了）
"""

import sys
from pathlib import Path

# 把 toutiao_backend 加入搜索路径
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import create_engine

from config.settings import settings

# ========== 1. 用同步引擎创建表（pymysql，避免异步事件循环问题）==========
sync_url = settings.database_url.replace("mysql+aiomysql://", "mysql+pymysql://")
sync_engine = create_engine(sync_url, echo=False)

# 导入所有模型（让它们注册到 Base.metadata）
import models.favorite  # noqa: E402,F401
import models.history  # noqa: E402,F401
import models.news  # noqa: E402,F401
import models.users  # noqa: E402,F401
from models import Base  # noqa: E402

print("📦 创建数据库表...")
Base.metadata.create_all(bind=sync_engine)
print("✅ 表创建完成")

# ========== 2. 种子数据（幂等：重复运行不会重复插入）==========
from sqlalchemy import text  # noqa: E402

with sync_engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM news_category"))
    count = result.scalar()
    if count > 0:
        print(f"ℹ️  已有 {count} 条分类数据，跳过种子数据")
        sync_engine.dispose()
        sys.exit(0)

    print("🌱 插入种子数据...")

    conn.execute(
        text("""
        INSERT INTO news_category (name, sort_order, created_at, updated_at) VALUES
        ('科技', 1, NOW(), NOW()),
        ('财经', 2, NOW(), NOW()),
        ('体育', 3, NOW(), NOW())
    """)
    )

    conn.execute(
        text("""
        INSERT INTO news (title, description, content, author, category_id, views, publish_time, created_at, updated_at) VALUES
        (
            'AI技术取得重大突破',
            '人工智能领域迎来新进展',
            '<p>这是测试新闻的详细内容，用于CI测试验证。</p>',
            '测试作者',
            1,
            100,
            NOW(),
            NOW(),
            NOW()
        ),
        (
            '全球股市今日动态',
            '各大股指涨跌不一',
            '<p>财经新闻的详细内容，用于CI测试验证。</p>',
            '财经记者',
            2,
            50,
            NOW(),
            NOW(),
            NOW()
        )
    """)
    )
    conn.commit()
    print("✅ 种子数据插入完成")

sync_engine.dispose()
print("🎉 测试数据库初始化完成")
