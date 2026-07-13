"""
测试基础设施 —— pytest 启动时自动加载

提供的 fixtures（测试夹具）:
  - client         FastAPI 同步测试客户端（模拟前端发请求）
  - test_user      自动注册一个测试用户，返回 token + 用户信息
"""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# 把 toutiao_backend 目录加入 Python 搜索路径
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import app


@pytest.fixture
def client():
    """
    测试客户端 —— FastAPI 官方推荐的 TestClient
    内部自动处理 async/await，你的测试代码写成同步的就行
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_user(client):
    """
    注册一个唯一的测试用户，返回 token 和用户信息
    每个测试拿到的是独立用户，不会互相干扰
    """
    import uuid

    unique_id = uuid.uuid4().hex[:8]
    username = f"test_{unique_id}"
    password = "test123456"

    resp = client.post(
        "/api/user/register",
        json={
            "username": username,
            "password": password,
        },
    )
    assert resp.status_code == 200, f"测试用户注册失败: {resp.text}"

    data = resp.json()["data"]
    token = data["token"]
    user_info = data["userInfo"]

    return {
        "token": token,
        "username": username,
        "password": password,
        "user_info": user_info,
    }
