"""
用户接口测试 —— 覆盖注册、登录、获取信息

使用 FastAPI 官方 TestClient（同步写法，自动处理异步）
"""


# ==================== 注册接口 ====================


def test_register_success(client):
    """✅ 正确注册：返回 token + 用户信息"""
    resp = client.post(
        "/api/user/register",
        json={
            "username": "testuser_001",
            "password": "abc123",
        },
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert "token" in data
    assert data["userInfo"]["username"] == "testuser_001"


def test_register_duplicate_username(client):
    """❌ 重复注册：应返回 400"""
    # 第一次注册
    client.post(
        "/api/user/register",
        json={
            "username": "dup_user_xyz",
            "password": "abc123",
        },
    )
    # 第二次用同一用户名注册
    resp = client.post(
        "/api/user/register",
        json={
            "username": "dup_user_xyz",
            "password": "abc123",
        },
    )
    assert resp.status_code == 400
    assert "已存在" in resp.json()["message"]


# ==================== 登录接口 ====================


def test_login_success(client, test_user):
    """✅ 正确登录：返回 token"""
    resp = client.post(
        "/api/user/login",
        json={
            "username": test_user["username"],
            "password": test_user["password"],
        },
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert "token" in data
    assert data["userInfo"]["username"] == test_user["username"]


def test_login_wrong_password(client, test_user):
    """❌ 密码错误：应返回 401"""
    resp = client.post(
        "/api/user/login",
        json={
            "username": test_user["username"],
            "password": "wrong_password",
        },
    )
    assert resp.status_code == 401


def test_login_user_not_exist(client):
    """❌ 用户不存在：应返回 401"""
    resp = client.post(
        "/api/user/login",
        json={
            "username": "no_such_user_99999",
            "password": "abc123",
        },
    )
    assert resp.status_code == 401


# ==================== 获取用户信息 ====================


def test_get_user_info_with_token(client, test_user):
    """✅ 有有效 token：返回用户信息"""
    resp = client.get(
        "/api/user/info",
        headers={
            "Authorization": f"Bearer {test_user['token']}",
        },
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["username"] == test_user["username"]


def test_get_user_info_without_token(client):
    """❌ 没有 token：FastAPI 校验 Header 缺失 → 422"""
    resp = client.get("/api/user/info")
    # FastAPI 的 Header(..., alias="Authorization") 是必填项
    # 缺少 header 时先触发参数校验错误（422）
    assert resp.status_code == 422


# ==================== 修改密码 ====================


def test_change_password(client, test_user):
    """✅ 修改密码后用新密码登录成功"""
    # 修改密码
    resp = client.put(
        "/api/user/password",
        json={
            "oldPassword": test_user["password"],
            "newPassword": "newpwd123",
        },
        headers={
            "Authorization": f"Bearer {test_user['token']}",
        },
    )
    assert resp.status_code == 200

    # 用新密码登录
    resp = client.post(
        "/api/user/login",
        json={
            "username": test_user["username"],
            "password": "newpwd123",
        },
    )
    assert resp.status_code == 200


def test_change_password_wrong_old(client, test_user):
    """❌ 旧密码错误：应返回 500"""
    resp = client.put(
        "/api/user/password",
        json={
            "oldPassword": "wrong_old_pwd",
            "newPassword": "newpwd123",
        },
        headers={
            "Authorization": f"Bearer {test_user['token']}",
        },
    )
    assert resp.status_code == 500
