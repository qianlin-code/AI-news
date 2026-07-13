# API 接口规范文档

## 概述

新闻资讯系统 RESTful API，提供用户管理、新闻浏览、收藏和历史记录功能。

## 基础信息

- **Base URL**: `http://127.0.0.1:8000`
- **认证方式**: 请求头 `Authorization: <token值>`（支持 `Bearer <token>` 格式）
- **Content-Type**: `application/json`
- **响应格式**: 统一 `{ "code": 200, "message": "success", "data": {...} }`

## 通用说明

| 场景 | HTTP 状态码 | 响应示例 |
|------|-------------|----------|
| 成功 | 200 | `{"code":200, "message":"success", "data":{...}}` |
| 参数校验失败 | 422 | `{"code":422, "message":"...", "data":null}` |
| 未登录/Token过期 | 401 | `{"code":401, "message":"...", "data":null}` |
| 资源不存在 | 404 | `{"code":404, "message":"...", "data":null}` |
| 服务器错误 | 500 | `{"code":500, "message":"...", "data":null}` |

---

## 一、用户模块 `/api/user`

### 1. 用户注册

```
POST /api/user/register
```

**请求体：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名（唯一） |
| password | string | 是 | 密码 |

**请求示例：**
```json
{
  "username": "test_user",
  "password": "123456"
}
```

**响应示例：**
```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "token": "a1b2c3d4-...",
    "userInfo": {
      "id": 1,
      "username": "test_user",
      "nickname": null,
      "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg",
      "gender": "unknown",
      "bio": "这个人很懒, 什么都没留下"
    }
  }
}
```

### 2. 用户登录

```
POST /api/user/login
```

**请求体：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |

**请求示例：**
```json
{
  "username": "test_user",
  "password": "123456"
}
```

**响应示例：**
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "a1b2c3d4-...",
    "userInfo": {
      "id": 1,
      "username": "test_user",
      "nickname": null,
      "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg",
      "gender": "unknown",
      "bio": "这个人很懒, 什么都没留下"
    }
  }
}
```

### 3. 获取用户信息 🔒

```
GET /api/user/info
Authorization: <token>
```

**响应示例：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "username": "test_user",
    "nickname": null,
    "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg",
    "gender": "unknown",
    "bio": "这个人很懒, 什么都没留下"
  }
}
```

### 4. 更新用户信息 🔒

```
PUT /api/user/update
Authorization: <token>
```

**请求体（全部可选，只更新传了的字段）：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| nickname | string | 否 | 昵称 |
| avatar | string | 否 | 头像 URL |
| gender | string | 否 | 性别：male / female / unknown |
| bio | string | 否 | 个人简介 |
| phone | string | 否 | 手机号 |

**请求示例：**
```json
{
  "bio": "这是我的个人简介",
  "nickname": "小明"
}
```

**响应示例：**
```json
{
  "code": 200,
  "message": "更新成功",
  "data": {
    "id": 1,
    "username": "test_user",
    "nickname": "小明",
    "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg",
    "gender": "unknown",
    "bio": "这是我的个人简介"
  }
}
```

### 5. 修改密码 🔒

```
PUT /api/user/password
Authorization: <token>
```

**请求体：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| oldPassword | string | 是 | 当前密码 |
| newPassword | string | 是 | 新密码（最少 6 位） |

**请求示例：**
```json
{
  "oldPassword": "123456",
  "newPassword": "654321"
}
```

**响应示例：**
```json
{
  "code": 200,
  "message": "密码修改成功",
  "data": null
}
```

---

## 二、新闻模块 `/api/news`

### 1. 获取新闻分类列表

```
GET /api/news/categories
GET /api/news/categories?skip=0&limit=10
```

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| skip | int | 否 | 0 | 跳过条数 |
| limit | int | 否 | 100 | 返回条数 |

**响应示例：**
```json
{
  "code": 200,
  "message": "获取新闻分类成功",
  "data": [
    {
      "id": 1,
      "name": "科技",
      "sort_order": 0,
      "created_at": "2026-07-13T10:00:00",
      "updated_at": "2026-07-13T10:00:00"
    }
  ]
}
```

### 2. 获取新闻列表

```
GET /api/news/list?categoryId=1
GET /api/news/list?categoryId=1&page=2&pageSize=20
```

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| categoryId | int | 是 | — | 分类 ID |
| page | int | 否 | 1 | 页码 |
| pageSize | int | 否 | 10 | 每页条数（最大 100） |

**响应示例：**
```json
{
  "code": 200,
  "message": "获取新闻列表成功",
  "data": {
    "list": [
      {
        "id": 1,
        "title": "新闻标题",
        "description": "新闻简介",
        "image": null,
        "author": "作者名",
        "categoryId": 1,
        "views": 100,
        "publishedTime": "2026-07-13T08:00:00"
      }
    ],
    "total": 50,
    "hasMore": true
  }
}
```

### 3. 获取新闻详情

```
GET /api/news/detail?id=1
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 新闻 ID |

**响应示例：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "title": "新闻标题",
    "content": "新闻正文内容...",
    "image": null,
    "author": "作者名",
    "publishTime": "2026-07-13T08:00:00",
    "categoryId": 1,
    "views": 101,
    "relatedNews": [
      {
        "id": 2,
        "title": "相关新闻标题",
        "content": "相关新闻内容...",
        "image": null,
        "author": "作者名",
        "publishTime": "2026-07-13T07:00:00",
        "categoryId": 1,
        "views": 50
      }
    ]
  }
}
```

> `relatedNews` 为同分类下按浏览量和发布时间排序的 Top 5 新闻，带 Redis 缓存（2 分钟过期）。

---

## 三、收藏模块 `/api/favorite`

> 所有收藏接口需要认证 🔒

### 1. 检查收藏状态

```
GET /api/favorite/check?newsId=1
Authorization: <token>
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| newsId | int | 是 | 新闻 ID |

**响应示例：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "isFavorite": true
  }
}
```

### 2. 添加收藏

```
POST /api/favorite/add
Authorization: <token>
```

**请求体：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| newsId | int | 是 | 新闻 ID |

**请求示例：**
```json
{
  "newsId": 1
}
```

**响应示例：**
```json
{
  "code": 200,
  "message": "收藏成功",
  "data": {
    "id": 1,
    "userId": 1,
    "newsId": 1,
    "createTime": "2026-07-13T10:00:00"
  }
}
```

### 3. 取消收藏

```
DELETE /api/favorite/remove?newsId=1
Authorization: <token>
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| newsId | int | 是 | 新闻 ID |

**响应示例：**
```json
{
  "code": 200,
  "message": "取消收藏成功",
  "data": null
}
```

### 4. 获取收藏列表

```
GET /api/favorite/list
GET /api/favorite/list?page=1&pageSize=10
Authorization: <token>
```

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| page | int | 否 | 1 | 页码 |
| pageSize | int | 否 | 10 | 每页条数（最大 100） |

**响应示例：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "list": [
      {
        "id": 1,
        "title": "收藏的新闻标题",
        "description": "新闻简介",
        "image": null,
        "author": "作者名",
        "publishTime": "2026-07-13T08:00:00",
        "categoryId": 1,
        "views": 100,
        "favoriteId": 10,
        "favoriteTime": "2026-07-13T11:00:00"
      }
    ],
    "total": 1,
    "hasMore": false
  }
}
```

### 5. 清空所有收藏

```
DELETE /api/favorite/clear
Authorization: <token>
```

**响应示例：**
```json
{
  "code": 200,
  "message": "成功删除 3 条收藏记录",
  "data": null
}
```

---

## 四、浏览历史模块 `/api/history`

> 所有历史接口需要认证 🔒

### 1. 添加浏览记录

```
POST /api/history/add
Authorization: <token>
```

**请求体：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| newsId | int | 是 | 新闻 ID |

**请求示例：**
```json
{
  "newsId": 1
}
```

**响应示例：**
```json
{
  "code": 200,
  "message": "添加成功",
  "data": {
    "id": 1,
    "userId": 1,
    "newsId": 1,
    "viewTime": "2026-07-13T12:00:00"
  }
}
```

> 去重策略：如果该用户已浏览过该新闻，则更新 `viewTime` 而非新增记录。

### 2. 获取浏览历史列表

```
GET /api/history/list
GET /api/history/list?page=1&pageSize=10
Authorization: <token>
```

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| page | int | 否 | 1 | 页码 |
| pageSize | int | 否 | 10 | 每页条数（最大 100） |

**响应示例：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "list": [
      {
        "id": 1,
        "title": "浏览过的新闻标题",
        "description": "新闻简介",
        "image": null,
        "author": "作者名",
        "publishTime": "2026-07-13T08:00:00",
        "categoryId": 1,
        "views": 100,
        "viewTime": "2026-07-13T12:00:00"
      }
    ],
    "total": 20,
    "hasMore": true
  }
}
```

### 3. 删除单条浏览记录

```
DELETE /api/history/delete/{history_id}
Authorization: <token>
```

**路径参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| history_id | int | 是 | 历史记录 ID |

**请求示例：**
```
DELETE /api/history/delete/1
```

**响应示例：**
```json
{
  "code": 200,
  "message": "删除成功",
  "data": null
}
```

### 4. 清空浏览历史

```
DELETE /api/history/clear
Authorization: <token>
```

**响应示例：**
```json
{
  "code": 200,
  "message": "成功清空 20 条浏览记录",
  "data": null
}
```
