import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import reverse
from django.conf import settings
from django.utils.http import url_has_allowed_host_and_scheme


@method_decorator(csrf_exempt, name='dispatch')
class APIDocumentationView(View):
    """API文档接口"""
    
    def get(self, request):
        """获取所有API接口文档"""
        try:
            # 获取查询参数
            format_type = request.GET.get('format', 'json')  # json, swagger, openapi
            group = request.GET.get('group', 'all')  # all, auth, user, docs
            
            # 基础文档信息
            api_info = {
                "info": {
                    "title": "Django RESTful API",
                    "version": "1.0.0",
                    "description": "基于Django的RESTful API接口文档",
                    "contact": {
                        "name": "API Support",
                        "email": "support@example.com"
                    },
                    "license": {
                        "name": "MIT",
                        "url": "https://opensource.org/licenses/MIT"
                    }
                },
                "servers": [
                    {
                        "url": "http://localhost:8000",
                        "description": "开发环境"
                    },
                    {
                        "url": "https://api.example.com",
                        "description": "生产环境"
                    }
                ],
                "security": [
                    {
                        "BearerAuth": []
                    }
                ],
                "components": {
                    "securitySchemes": {
                        "BearerAuth": {
                            "type": "http",
                            "scheme": "bearer",
                            "bearerFormat": "JWT"
                        }
                    },
                    "schemas": {
                        "User": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "string",
                                    "format": "uuid",
                                    "description": "用户唯一标识"
                                },
                                "username": {
                                    "type": "string",
                                    "description": "用户名"
                                },
                                "email": {
                                    "type": "string",
                                    "format": "email",
                                    "description": "邮箱地址"
                                },
                                "real_name": {
                                    "type": "string",
                                    "description": "真实姓名"
                                },
                                "user_role": {
                                    "type": "string",
                                    "enum": ["admin", "normal", "vip"],
                                    "description": "用户角色"
                                },
                                "is_active": {
                                    "type": "boolean",
                                    "description": "是否激活"
                                },
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "创建时间"
                                }
                            }
                        },
                        "SuccessResponse": {
                            "type": "object",
                            "properties": {
                                "code": {
                                    "type": "integer",
                                    "description": "状态码"
                                },
                                "msg": {
                                    "type": "string",
                                    "description": "响应消息"
                                },
                                "data": {
                                    "description": "响应数据"
                                }
                            }
                        },
                        "ErrorResponse": {
                            "type": "object",
                            "properties": {
                                "code": {
                                    "type": "integer",
                                    "description": "错误码"
                                },
                                "msg": {
                                    "type": "string",
                                    "description": "错误消息"
                                },
                                "errors": {
                                    "type": "object",
                                    "description": "详细错误信息"
                                }
                            }
                        }
                    }
                }
            }
            
            # API路径定义
            paths = {
                "/auth/register/": {
                    "post": {
                        "tags": ["认证"],
                        "summary": "用户注册",
                        "description": "创建新用户账户",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["username", "password", "password_confirm", "email"],
                                        "properties": {
                                            "username": {
                                                "type": "string",
                                                "minLength": 3,
                                                "maxLength": 50,
                                                "description": "用户名，至少3位"
                                            },
                                            "password": {
                                                "type": "string",
                                                "minLength": 8,
                                                "description": "密码，至少8位，必须包含字母和数字"
                                            },
                                            "password_confirm": {
                                                "type": "string",
                                                "description": "确认密码"
                                            },
                                            "email": {
                                                "type": "string",
                                                "format": "email",
                                                "description": "邮箱地址"
                                            },
                                            "real_name": {
                                                "type": "string",
                                                "maxLength": 100,
                                                "description": "真实姓名"
                                            },
                                            "gender": {
                                                "type": "string",
                                                "enum": ["男", "女"],
                                                "description": "性别"
                                            },
                                            "phone_number": {
                                                "type": "string",
                                                "pattern": "^1[3-9]\\d{9}$",
                                                "description": "手机号码"
                                            }
                                        }
                                    },
                                    "example": {
                                        "username": "testuser",
                                        "password": "Test123456",
                                        "password_confirm": "Test123456",
                                        "email": "test@example.com",
                                        "real_name": "测试用户",
                                        "phone_number": "13800138000"
                                    }
                                }
                            }
                        },
                        "responses": {
                            "201": {
                                "description": "注册成功",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/SuccessResponse"
                                        },
                                        "example": {
                                            "code": 201,
                                            "msg": "注册成功",
                                            "data": {
                                                "user": {
                                                    "id": "550e8400-e29b-41d4-a716-446655440000",
                                                    "username": "testuser",
                                                    "email": "test@example.com",
                                                    "user_role": "normal"
                                                },
                                                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                                                "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                                                "token_type": "Bearer",
                                                "expires_in": 3600
                                            }
                                        }
                                    }
                                }
                            },
                            "400": {
                                "description": "请求参数错误",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/ErrorResponse"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "/auth/login/": {
                    "post": {
                        "tags": ["认证"],
                        "summary": "用户登录",
                        "description": "用户身份验证并获取访问令牌",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["username", "password"],
                                        "properties": {
                                            "username": {
                                                "type": "string",
                                                "description": "用户名或邮箱"
                                            },
                                            "password": {
                                                "type": "string",
                                                "description": "密码"
                                            }
                                        }
                                    },
                                    "example": {
                                        "username": "testuser",
                                        "password": "Test123456"
                                    }
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "description": "登录成功",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/SuccessResponse"
                                        },
                                        "example": {
                                            "code": 200,
                                            "msg": "登录成功",
                                            "data": {
                                                "user": {
                                                    "id": "550e8400-e29b-41d4-a716-446655440000",
                                                    "username": "testuser",
                                                    "email": "test@example.com",
                                                    "user_role": "normal",
                                                    "login_count": 5
                                                },
                                                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                                                "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                                                "token_type": "Bearer",
                                                "expires_in": 3600
                                            }
                                        }
                                    }
                                }
                            },
                            "401": {
                                "description": "认证失败",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/ErrorResponse"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "/auth/logout/": {
                    "post": {
                        "tags": ["认证"],
                        "summary": "用户登出",
                        "description": "退出当前用户会话",
                        "security": [{"BearerAuth": []}],
                        "responses": {
                            "200": {
                                "description": "登出成功",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "code": 200,
                                            "msg": "登出成功"
                                        }
                                    }
                                }
                            },
                            "401": {
                                "description": "未认证",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/ErrorResponse"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "/auth/user/": {
                    "get": {
                        "tags": ["用户管理"],
                        "summary": "获取当前用户信息",
                        "description": "获取当前登录用户的详细信息",
                        "security": [{"BearerAuth": []}],
                        "responses": {
                            "200": {
                                "description": "获取成功",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/SuccessResponse"
                                        }
                                    }
                                }
                            },
                            "401": {
                                "description": "未认证",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/ErrorResponse"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "put": {
                        "tags": ["用户管理"],
                        "summary": "更新用户资料",
                        "description": "更新当前登录用户的个人信息",
                        "security": [{"BearerAuth": []}],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "real_name": {"type": "string"},
                                            "gender": {"type": "string", "enum": ["男", "女"]},
                                            "phone_number": {"type": "string"},
                                            "avatar": {"type": "string"},
                                            "signature": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "description": "更新成功",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/SuccessResponse"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "/auth/password/change/": {
                    "post": {
                        "tags": ["用户管理"],
                        "summary": "修改密码",
                        "description": "修改当前用户的登录密码",
                        "security": [{"BearerAuth": []}],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["old_password", "new_password", "new_password_confirm"],
                                        "properties": {
                                            "old_password": {
                                                "type": "string",
                                                "description": "旧密码"
                                            },
                                            "new_password": {
                                                "type": "string",
                                                "minLength": 8,
                                                "description": "新密码"
                                            },
                                            "new_password_confirm": {
                                                "type": "string",
                                                "description": "确认新密码"
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "description": "密码修改成功",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "code": 200,
                                            "msg": "密码修改成功"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "/auth/users/": {
                    "get": {
                        "tags": ["用户管理"],
                        "summary": "获取用户列表",
                        "description": "获取系统用户列表（管理员权限）",
                        "security": [{"BearerAuth": []}],
                        "parameters": [
                            {
                                "name": "page",
                                "in": "query",
                                "schema": {"type": "integer", "default": 1},
                                "description": "页码"
                            },
                            {
                                "name": "page_size",
                                "in": "query",
                                "schema": {"type": "integer", "default": 10},
                                "description": "每页数量"
                            },
                            {
                                "name": "search",
                                "in": "query",
                                "schema": {"type": "string"},
                                "description": "搜索关键词"
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "获取成功",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "code": 200,
                                            "msg": "获取用户列表成功",
                                            "data": {
                                                "users": [
                                                    {
                                                        "id": "550e8400-e29b-41d4-a716-446655440000",
                                                        "username": "testuser",
                                                        "email": "test@example.com",
                                                        "user_role": "normal"
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
                                    }
                                }
                            },
                            "403": {
                                "description": "权限不足",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/ErrorResponse"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "/docs/api/": {
                    "get": {
                        "tags": ["文档"],
                        "summary": "获取API文档",
                        "description": "获取完整的API接口文档",
                        "parameters": [
                            {
                                "name": "format",
                                "in": "query",
                                "schema": {
                                    "type": "string",
                                    "enum": ["json", "swagger", "openapi"],
                                    "default": "json"
                                },
                                "description": "文档格式"
                            },
                            {
                                "name": "group",
                                "in": "query",
                                "schema": {
                                    "type": "string",
                                    "enum": ["all", "auth", "user", "docs"],
                                    "default": "all"
                                },
                                "description": "接口分组"
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "获取成功",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/SuccessResponse"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            
            # 根据分组过滤
            if group != 'all':
                filtered_paths = {}
                for path, methods in paths.items():
                    for method, details in methods.items():
                        if 'tags' in details:
                            if (group == 'auth' and '认证' in details['tags']) or \
                               (group == 'user' and '用户管理' in details['tags']) or \
                               (group == 'docs' and '文档' in details['tags']):
                                if path not in filtered_paths:
                                    filtered_paths[path] = {}
                                filtered_paths[path][method] = details
                paths = filtered_paths
            
            # 组装最终文档
            api_docs = {**api_info, "paths": paths}
            
            # 添加额外信息
            api_docs["meta"] = {
                "generated_at": "2024-01-01T12:00:00Z",
                "total_endpoints": len(paths),
                "groups": {
                    "认证": ["/auth/register/", "/auth/login/", "/auth/logout/"],
                    "用户管理": ["/auth/user/", "/auth/password/change/", "/auth/users/"],
                    "文档": ["/docs/api/"]
                },
                "common_errors": {
                    "400": "请求参数错误",
                    "401": "未认证或token无效",
                    "403": "权限不足",
                    "404": "资源不存在",
                    "500": "服务器内部错误"
                },
                "response_format": {
                    "success": {
                        "code": 200,
                        "msg": "成功消息",
                        "data": {}
                    },
                    "error": {
                        "code": 400,
                        "msg": "错误消息",
                        "errors": {}
                    }
                }
            }
            
            return JsonResponse({
                'code': 200,
                'msg': '获取API文档成功',
                'data': api_docs
            })
            
        except Exception as e:
            return JsonResponse({
                'code': 500,
                'msg': f'获取API文档失败: {str(e)}'
            }, status=500)