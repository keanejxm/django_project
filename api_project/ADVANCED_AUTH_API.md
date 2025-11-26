# 高级JWT用户认证 API 文档

## 概述
本项目提供了企业级的JWT用户认证系统，支持完整的用户管理功能，包括注册、登录、资料管理、密码修改等。

## 基础信息
- **基础URL**: `http://localhost:8000`
- **认证方式**: JWT Bearer Token
- **数据格式**: JSON
- **字符编码**: UTF-8
- **用户模型**: 自定义User模型（UUID主键）

## 用户模型特性

### 核心字段
- **id**: UUID主键
- **username**: 用户名（唯一，50字符）
- **real_name**: 真实姓名
- **email**: 邮箱（唯一）
- **phone_number**: 手机号（11位）
- **gender**: 性别（男/女）
- **date_of_birth**: 出生日期
- **avatar**: 头像URL
- **signature**: 个性签名

### 安全字段
- **password**: 加密密码
- **salt**: 密码盐值
- **login_count**: 登录次数
- **last_login_time**: 最后登录时间

### 权限字段
- **user_role**: 用户角色（admin/normal/vip）
- **permission_flags**: 权限标识
- **is_active**: 账户状态

## 接口列表

### 1. 用户注册

- **URL**: `/api/auth/register/`
- **方法**: POST
- **描述**: 新用户注册，支持完整用户信息

**请求参数**:
```json
{
    "username": "advanced_user",
    "password": "Advanced123",
    "password_confirm": "Advanced123",
    "email": "user@example.com",
    "real_name": "张三",
    "gender": "男",
    "date_of_birth": "1990-01-01",
    "phone_number": "13800138000"
}
```

**验证规则**:
- 用户名：3-50字符，唯一
- 密码：至少8位，包含字母和数字
- 邮箱：格式正确，唯一
- 手机号：11位数字（可选）

**响应示例**:
```json
{
    "code": 201,
    "msg": "注册成功",
    "data": {
        "user": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "username": "advanced_user",
            "real_name": "张三",
            "email": "user@example.com",
            "gender": "男",
            "gender_display": "男",
            "user_role": "normal",
            "user_role_display": "普通用户",
            "login_count": 0,
            "registration_time": "2023-01-01T00:00:00Z"
        },
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "token_type": "Bearer",
        "expires_in": 3600
    }
}
```

### 2. 用户登录

- **URL**: `/api/auth/login/`
- **方法**: POST
- **描述**: 用户登录认证，自动更新登录统计

**请求参数**:
```json
{
    "username": "advanced_user",
    "password": "Advanced123"
}
```

**响应示例**:
```json
{
    "code": 200,
    "msg": "登录成功",
    "data": {
        "user": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "username": "advanced_user",
            "login_count": 5,
            "last_login_time": "2023-01-01T12:00:00Z"
        },
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "token_type": "Bearer",
        "expires_in": 3600
    }
}
```

### 3. 获取/更新用户信息

- **URL**: `/api/auth/userinfo/`
- **方法**: GET / PUT
- **描述**: 获取或更新当前用户信息

**GET请求**（无需额外参数）:
```http
Authorization: Bearer <access_token>
```

**PUT请求参数**:
```json
{
    "real_name": "李四",
    "gender": "女",
    "date_of_birth": "1992-05-15",
    "phone_number": "13900139000",
    "avatar": "https://example.com/new-avatar.jpg",
    "signature": "新的个性签名",
    "remark": "备注信息"
}
```

**响应示例**:
```json
{
    "code": 200,
    "msg": "获取用户信息成功",
    "data": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "username": "advanced_user",
        "real_name": "李四",
        "email": "user@example.com",
        "gender": "女",
        "gender_display": "女",
        "date_of_birth": "1992-05-15",
        "phone_number": "13900139000",
        "avatar": "https://example.com/new-avatar.jpg",
        "signature": "新的个性签名",
        "user_role": "normal",
        "user_role_display": "普通用户",
        "login_count": 5,
        "last_login_time": "2023-01-01T12:00:00Z",
        "is_active": true
    }
}
```

### 4. 修改密码

- **URL**: `/api/auth/password/change/`
- **方法**: POST
- **描述**: 修改当前用户密码

**请求参数**:
```json
{
    "old_password": "OldPassword123",
    "new_password": "NewPassword456",
    "new_password_confirm": "NewPassword456"
}
```

**验证规则**:
- 旧密码必须正确
- 新密码至少8位，包含字母和数字
- 两次输入的新密码必须一致

**响应示例**:
```json
{
    "code": 200,
    "msg": "密码修改成功"
}
```

### 5. Token刷新

- **URL**: `/api/auth/token/refresh/`
- **方法**: POST
- **描述**: 使用refresh token获取新的access token

**请求参数**:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**响应示例**:
```json
{
    "code": 200,
    "msg": "Token刷新成功",
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "token_type": "Bearer",
        "expires_in": 3600
    }
}
```

### 6. 用户登出

- **URL**: `/api/auth/logout/`
- **方法**: POST
- **描述**: 用户登出，使token失效

**请求头**:
```http
Authorization: Bearer <access_token>
```

**响应示例**:
```json
{
    "code": 200,
    "msg": "登出成功"
}
```

### 7. 用户列表（管理员）

- **URL**: `/api/auth/users/`
- **方法**: GET
- **描述**: 获取用户列表（仅管理员）

**请求参数**:
- `page`: 页码（默认1）
- `page_size`: 每页数量（默认10）
- `search`: 搜索关键词

**请求头**:
```http
Authorization: Bearer <access_token>
```

**响应示例**:
```json
{
    "code": 200,
    "msg": "获取用户列表成功",
    "data": {
        "users": [
            {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "username": "admin",
                "real_name": "管理员",
                "email": "admin@example.com",
                "user_role": "admin",
                "user_role_display": "管理员",
                "login_count": 100,
                "is_active": true
            }
        ],
        "pagination": {
            "page": 1,
            "page_size": 10,
            "total": 1,
            "pages": 1
        }
    }
}
```

## 状态码说明

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 用户未认证或token无效 |
| 403 | 权限不足 |
| 500 | 服务器内部错误 |

## 安全特性

### 1. 密码安全
- **加密存储**: Django内置密码哈希
- **盐值加密**: 每个用户独立salt
- **复杂度验证**: 字母+数字，至少8位
- **密码历史**: 修改密码需验证旧密码

### 2. JWT安全
- **HMAC-SHA256** 签名算法
- **短期Token**: Access Token 1小时
- **长期Token**: Refresh Token 7天
- **自动轮换**: Refresh Token使用后自动更换

### 3. 访问控制
- **角色权限**: admin/normal/vip三级权限
- **接口保护**: 所有敏感接口需要认证
- **权限检查**: 管理员功能权限验证

## 使用示例

### 注册新用户
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "NewUser123",
    "password_confirm": "NewUser123",
    "email": "newuser@example.com",
    "real_name": "新用户",
    "gender": "男"
  }'
```

### 用户登录
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","password":"NewUser123"}'
```

### 更新用户资料
```bash
curl -X PUT http://localhost:8000/api/auth/userinfo/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "real_name": "更新后的姓名",
    "signature": "我的新签名"
  }'
```

### 修改密码
```bash
curl -X POST http://localhost:8000/api/auth/password/change/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "old_password": "NewUser123",
    "new_password": "NewPassword456",
    "new_password_confirm": "NewPassword456"
  }'
```

## 测试说明

### 运行测试脚本
```bash
python test_advanced_auth.py
```

### 测试覆盖
- ✅ 完整用户注册
- ✅ 用户登录统计
- ✅ 用户信息获取/更新
- ✅ 密码修改
- ✅ Token刷新
- ✅ 输入验证
- ✅ 权限控制
- ✅ 错误处理

## 前端集成示例

### React组件示例
```javascript
// 用户注册
const register = async (userData) => {
  const response = await fetch('/api/auth/register/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
  });
  return response.json();
};

// 更新用户资料
const updateProfile = async (profileData) => {
  const token = localStorage.getItem('access_token');
  const response = await fetch('/api/auth/userinfo/', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(profileData)
  });
  return response.json();
};

// 修改密码
const changePassword = async (passwordData) => {
  const token = localStorage.getItem('access_token');
  const response = await fetch('/api/auth/password/change/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(passwordData)
  });
  return response.json();
};
```

## 生产环境建议

1. **HTTPS**: 强制使用HTTPS
2. **限流**: 实现API请求限流
3. **监控**: 添加登录异常监控
4. **审计**: 记录敏感操作日志
5. **备份**: 定期备份用户数据
6. **加密**: 敏感字段加密存储

## 技术栈

- **Django**: 5.0
- **Django REST Framework**: 3.14.0
- **Simple JWT**: 5.3.0
- **UUID**: 主键标识
- **PostgreSQL**: 推荐生产数据库