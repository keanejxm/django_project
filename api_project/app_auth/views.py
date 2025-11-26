import json
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from .serializers import (LoginSerializer, RegisterSerializer, UserSerializer, 
                         TokenRefreshSerializer, UserProfileSerializer, 
                         PasswordChangeSerializer)
from functools import wraps
from django.utils import timezone

User = get_user_model()


def jwt_required(view_func):
    """JWT认证装饰器"""
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({
                'code': 401,
                'msg': '缺少认证token'
            }, status=401)
        
        token = auth_header.split(' ')[1]
        try:
            # 验证token
            from rest_framework_simplejwt.authentication import JWTAuthentication
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(token)
            request.user = jwt_auth.get_user(validated_token)
            return view_func(request, *args, **kwargs)
        except (TokenError, InvalidToken) as e:
            return JsonResponse({
                'code': 401,
                'msg': 'Token无效或已过期'
            }, status=401)
    
    return wrapped_view


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    """用户登录视图"""
    
    def post(self, request):
        """用户登录接口"""
        try:
            data = json.loads(request.body)
            serializer = LoginSerializer(data=data)
            
            if serializer.is_valid():
                result = serializer.save()
                user = result['user']
                login(request, user)
                
                # 返回JWT tokens和用户信息
                user_serializer = UserSerializer(user)
                return JsonResponse({
                    'code': 200,
                    'msg': '登录成功',
                    'data': {
                        'user': user_serializer.data,
                        'access_token': result['access'],
                        'refresh_token': result['refresh'],
                        'token_type': 'Bearer',
                        'expires_in': 3600
                    }
                })
            else:
                return JsonResponse({
                    'code': 400,
                    'msg': '登录失败',
                    'errors': serializer.errors
                }, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'code': 400,
                'msg': '请求数据格式错误'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'code': 500,
                'msg': f'服务器内部错误: {str(e)}'
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(View):
    """用户登出视图"""
    
    @jwt_required
    def post(self, request):
        """用户登出接口"""
        try:
            # 将refresh token加入黑名单
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if auth_header and auth_header.startswith('Bearer '):
                # 这里可以进一步处理token黑名单
                pass
            
            logout(request)
            return JsonResponse({
                'code': 200,
                'msg': '登出成功'
            })
        except Exception as e:
            return JsonResponse({
                'code': 500,
                'msg': f'登出失败: {str(e)}'
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    """用户注册视图"""
    
    def post(self, request):
        """用户注册接口"""
        try:
            data = json.loads(request.body)
            serializer = RegisterSerializer(data=data)
            
            if serializer.is_valid():
                user = serializer.save()
                
                # 注册成功后自动登录并返回token
                refresh = RefreshToken.for_user(user)
                user_serializer = UserSerializer(user)
                
                return JsonResponse({
                    'code': 201,
                    'msg': '注册成功',
                    'data': {
                        'user': user_serializer.data,
                        'access_token': str(refresh.access_token),
                        'refresh_token': str(refresh),
                        'token_type': 'Bearer',
                        'expires_in': 3600
                    }
                }, status=201)
            else:
                return JsonResponse({
                    'code': 400,
                    'msg': '注册失败',
                    'errors': serializer.errors
                }, status=400)
            
        except json.JSONDecodeError:
            return JsonResponse({
                'code': 400,
                'msg': '请求数据格式错误'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'code': 500,
                'msg': f'注册失败: {str(e)}'
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class UserInfoView(View):
    """获取用户信息视图"""
    
    @jwt_required
    def get(self, request):
        """获取当前登录用户信息"""
        user_serializer = UserSerializer(request.user)
        return JsonResponse({
            'code': 200,
            'msg': '获取用户信息成功',
            'data': user_serializer.data
        })
    
    @jwt_required
    def put(self, request):
        """更新用户资料"""
        try:
            data = json.loads(request.body)
            serializer = UserProfileSerializer(
                instance=request.user, 
                data=data, 
                partial=True
            )
            
            if serializer.is_valid():
                user = serializer.save()
                user_serializer = UserSerializer(user)
                return JsonResponse({
                    'code': 200,
                    'msg': '用户资料更新成功',
                    'data': user_serializer.data
                })
            else:
                return JsonResponse({
                    'code': 400,
                    'msg': '更新失败',
                    'errors': serializer.errors
                }, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'code': 400,
                'msg': '请求数据格式错误'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'code': 500,
                'msg': f'更新失败: {str(e)}'
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class TokenRefreshView(View):
    """Token刷新视图"""
    
    def post(self, request):
        """刷新access token"""
        try:
            data = json.loads(request.body)
            serializer = TokenRefreshSerializer(data=data)
            
            if serializer.is_valid():
                return JsonResponse({
                    'code': 200,
                    'msg': 'Token刷新成功',
                    'data': {
                        'access_token': serializer.validated_data['access'],
                        'token_type': 'Bearer',
                        'expires_in': 3600
                    }
                })
            else:
                return JsonResponse({
                    'code': 400,
                    'msg': 'Token刷新失败',
                    'errors': serializer.errors
                }, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'code': 400,
                'msg': '请求数据格式错误'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'code': 500,
                'msg': f'Token刷新失败: {str(e)}'
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class PasswordChangeView(View):
    """修改密码视图"""
    
    @jwt_required
    def post(self, request):
        """修改密码"""
        try:
            data = json.loads(request.body)
            serializer = PasswordChangeSerializer(
                data=data,
                context={'request': request}
            )
            
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({
                    'code': 200,
                    'msg': '密码修改成功'
                })
            else:
                return JsonResponse({
                    'code': 400,
                    'msg': '密码修改失败',
                    'errors': serializer.errors
                }, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'code': 400,
                'msg': '请求数据格式错误'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'code': 500,
                'msg': f'密码修改失败: {str(e)}'
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class UserListView(View):
    """用户列表视图（管理员功能）"""
    
    @jwt_required
    def get(self, request):
        """获取用户列表"""
        # 检查是否是管理员
        if not request.user.is_staff and request.user.user_role != 'admin':
            return JsonResponse({
                'code': 403,
                'msg': '权限不足'
            }, status=403)
        
        try:
            # 获取查询参数
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 10))
            search = request.GET.get('search', '')
            
            # 构建查询
            queryset = User.objects.all()
            if search:
                queryset = queryset.filter(
                    models.Q(username__icontains=search) |
                    models.Q(real_name__icontains=search) |
                    models.Q(email__icontains=search)
                )
            
            # 分页
            total = queryset.count()
            start = (page - 1) * page_size
            end = start + page_size
            users = queryset[start:end]
            
            # 序列化
            user_serializer = UserSerializer(users, many=True)
            
            return JsonResponse({
                'code': 200,
                'msg': '获取用户列表成功',
                'data': {
                    'users': user_serializer.data,
                    'pagination': {
                        'page': page,
                        'page_size': page_size,
                        'total': total,
                        'pages': (total + page_size - 1) // page_size
                    }
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'code': 500,
                'msg': f'获取用户列表失败: {str(e)}'
            }, status=500)