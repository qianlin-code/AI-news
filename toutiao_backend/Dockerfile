# ============================================
# Dockerfile — AI 掘金头条后端
# 基于 Python 3.12 slim 镜像
# ============================================
FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖（aiomysql、bcrypt 需要编译依赖）
# --no-install-recommends: 只装最小依赖，减小镜像体积
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc default-libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/*

# 先复制 requirements.txt（利用 Docker 缓存层）
# 只要 requirements.txt 没改，这层就能复用，不用每次都重装依赖
COPY requirements.txt .
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir -r requirements.txt

# 复制项目源码
COPY . .

# 容器内日志输出到 stdout（docker logs 能看）
ENV LOG_TO_CONSOLE=1

EXPOSE 8000

# 启动命令（0.0.0.0 是关键 —— 容器内必须绑定所有网络接口）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
