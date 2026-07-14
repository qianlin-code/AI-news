"""
健康检查接口测试
"""


def test_health_check(client):
    """✅ 健康检查：返回 ok 状态"""
    resp = client.get("/health")
    assert resp.status_code == 200

    json_data = resp.json()
    assert json_data["code"] == 200
    assert json_data["message"] == "服务运行正常"

    data = json_data["data"]
    assert data["status"] == "ok"
    assert data["service"] == "AI掘金头条"
    assert "uptime_seconds" in data
    assert isinstance(data["uptime_seconds"], (int, float))
    assert data["checks"]["api"] == "ok"


def test_health_method_not_allowed(client):
    """✅ POST /health 应该返回 405（只允许 GET）"""
    resp = client.post("/health")
    assert resp.status_code == 405
