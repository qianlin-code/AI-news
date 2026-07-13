# AI 掘金头条 — 新闻资讯全栈平台

基于 **FastAPI + Vue 3 + Redis + MySQL** 构建的新闻资讯系统，支持新闻分类浏览、详情阅读、AI 智能问答、用户收藏与浏览历史等核心功能。采用 **Cache-Aside 缓存模式** 提升响应速度，遵循企业级分层架构。

> 🎯 本项目为全栈学习作品，适合作为后端/全栈岗位实习求职项目展示。

## 技术栈

| 层级 | 技术 | 版本 |
| ------ | ------ | ------ |
| **后端框架** | FastAPI (async) | 0.139 |
| **前端框架** | Vue 3 + Vite | 7.x |
| **数据库** | MySQL 8 + SQLAlchemy 2.0 (async) | — |
| **缓存** | Redis (redis-py async) | 8.0 |
| **UI 组件库** | Vant 4 | 4.9 |
| **状态管理** | Pinia 3 | 3.0 |
| **AI 能力** | 阿里云通义千问 (qwen3-max) | — |
| **认证** | Bearer Token + bcrypt | — |
| **配置管理** | pydantic-settings + .env | 2.14 |

## 功能一览

- 🔐 **用户系统** — 注册 / 登录 / Token 鉴权 / 密码修改
- 📰 **新闻浏览** — 按分类分页浏览、关键词搜索、详情查看
- 🤖 **AI 智能问答** — 调用通义千问大模型，根据新闻内容进行智能问答
- ⭐ **收藏管理** — 收藏/取消收藏、收藏列表
- 🕘 **浏览历史** — 自动记录、去重更新、历史分页查询
- 📡 **相关推荐** — 同分类下相关新闻推荐
- ⚡ **Redis 缓存** — Cache-Aside 模式，启动预热，消除冷启动
- 📝 **统一日志** — 请求日志中间件 + 轮转文件日志
- 🛡️ **全局异常处理** — 分层捕获，开发/生产环境区分

## 项目截图

> 运行项目后访问 <http://127.0.0.1:5173> 即可体验。

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- MySQL 8.0+
- Redis（Windows 用户可用 [Memurai](https://www.memurai.com/) 或 Redis-x64）

### 1. 克隆项目

```bash
git clone https://github.com/qianlin-code/AI-news.git
cd AI-news
```

### 2. 配置后端

```bash
cd toutiao_backend

# 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate     # Windows
# source .venv/bin/activate  # macOS / Linux

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（复制模板后修改数据库密码）
copy .env.example .env
```

编辑 `.env`，填入你的 MySQL 密码：

```ini
DB_PASSWORD=你的MySQL密码
```

### 3. 配置前端

```bash
cd xwzx-news

# 安装依赖
npm install

# 配置环境变量（复制模板，填入 AI API Key）
copy .env.example .env
```

### 4. 一键启动（Windows）

双击项目根目录下的 `start.bat`，自动启动 Redis + 后端 + 前端。

或者手动分别启动：

```bash
# 终端1：启动 Redis
redis-server

# 终端2：启动后端 (端口 8000)
cd toutiao_backend
.venv\Scripts\activate
uvicorn main:app --host 127.0.0.1 --port 8000 --reload

# 终端3：启动前端 (端口 5173)
cd xwzx-news
npm run dev
```

### 5. 访问

- 前端页面：<http://127.0.0.1:5173>
- API 文档 (Swagger)：<http://127.0.0.1:8000/docs>

## 项目结构

```text
AI-news/
├── toutiao_backend/              # 后端项目
│   ├── main.py                   # 应用入口（FastAPI 实例化、生命周期）
│   ├── requirements.txt          # Python 依赖
│   ├── .env / .env.example       # 环境变量
│   ├── config/                   # 配置层
│   │   ├── settings.py           #   全局配置（pydantic-settings）
│   │   ├── db_conf.py            #   异步数据库引擎 + 会话工厂
│   │   ├── cache_conf.py         #   Redis 客户端
│   │   └── logger.py             #   统一日志
│   ├── models/                   # ORM 模型层（SQLAlchemy）
│   ├── schemas/                  # Pydantic 数据校验层
│   ├── crud/                     # 数据访问层（纯 DB 操作）
│   ├── cache/                    # 缓存 Key 管理 + 读写函数
│   ├── routers/                  # API 路由层
│   ├── middleware/                # 中间件（请求日志）
│   └── utils/                    # 工具（认证、加密、响应格式、异常处理）
│
├── xwzx-news/                    # 前端项目
│   ├── src/
│   │   ├── config/api.js         #   API 配置（环境变量）
│   │   ├── router/               #   路由配置
│   │   ├── store/                #   Pinia 状态管理
│   │   ├── views/                #   页面组件
│   │   └── utils/                #   工具函数
│   └── .env / .env.example       #   环境变量
│
├── start.bat                     # 一键启动脚本
├── 项目后端设计说明文档.md          # 后端设计文档
├── API接口规范文档.md              # API 接口文档
└── README.md
```

## 架构亮点

### Cache-Aside 缓存模式

```text
请求 → 查 Redis → 命中? → 返回 JSON
                  ↓ 未命中
             查 MySQL → 写 Redis → 返回 JSON
```

- 分类缓存 2 小时，新闻列表/详情 30 分钟，相关推荐 2 分钟
- **启动预热**：服务启动时自动将热门数据加载到 Redis，避免首个用户触发缓存冷启动

### 分层架构

```text
routers → crud → (cache ↔ models) → DB/Redis
   ↑         ↑
 schemas   utils（auth / security / response）
```

每层职责单一，不越界调用。路由层不直接操作数据库，数据访问层不处理 HTTP 逻辑。

### 统一异常处理

全局注册 5 级异常处理器：`RequestValidationError` → `HTTPException` → `IntegrityError` → `SQLAlchemyError` → `Exception`，开发环境返回堆栈，生产环境只返回提示语。

## 文档

- [后端设计说明文档](./项目后端设计说明文档.md)
- [API 接口规范文档](./API接口规范文档.md)

## License

MIT — 仅供学习交流使用。

---

> 💡 **面试提示**：本项目涵盖了企业级开发的核心理念——分层架构、缓存设计、日志系统、异常处理、配置管理、环境隔离。在面试中可以从这些角度展示你的工程化思维。
