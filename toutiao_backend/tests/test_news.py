"""
新闻接口测试 —— 覆盖分类、列表、详情

使用 FastAPI 官方 TestClient（同步写法，自动处理异步）
"""


# ==================== 分类接口 ====================


def test_get_categories(client):
    """✅ 获取分类列表：返回非空数据"""
    resp = client.get("/api/news/categories")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert isinstance(data, list)
    assert len(data) >= 1, "数据库里至少应有一个分类"
    for cat in data:
        assert "id" in cat
        assert "name" in cat


# ==================== 新闻列表接口 ====================


def test_get_news_list(client):
    """✅ 获取新闻列表：返回分页数据"""
    # 先获取第一个分类的 id
    cat_resp = client.get("/api/news/categories")
    categories = cat_resp.json()["data"]
    if not categories:
        return  # 没数据就跳过

    category_id = categories[0]["id"]

    resp = client.get(f"/api/news/list?categoryId={category_id}&page=1&pageSize=5")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert "list" in data
    assert "total" in data
    assert "hasMore" in data
    assert isinstance(data["list"], list)


def test_get_news_list_invalid_category(client):
    """✅ 不存在的分类：返回空列表"""
    resp = client.get("/api/news/list?categoryId=99999&page=1&pageSize=5")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["total"] == 0
    assert len(data["list"]) == 0


# ==================== 新闻详情接口 ====================


def test_get_news_detail(client):
    """✅ 获取新闻详情：返回完整信息（标题、内容、作者、相关推荐）"""
    # 先拿到一个新闻 id
    cat_resp = client.get("/api/news/categories")
    categories = cat_resp.json()["data"]
    if not categories:
        return

    list_resp = client.get(f"/api/news/list?categoryId={categories[0]['id']}&page=1&pageSize=1")
    news_list = list_resp.json()["data"]["list"]
    if not news_list:
        return

    news_id = news_list[0]["id"]

    resp = client.get(f"/api/news/detail?id={news_id}")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["id"] == news_id
    assert "title" in data
    assert "content" in data
    assert "author" in data
    assert "relatedNews" in data


def test_get_news_detail_not_found(client):
    """❌ 不存在的新闻：应返回 404"""
    resp = client.get("/api/news/detail?id=99999")
    assert resp.status_code == 404
