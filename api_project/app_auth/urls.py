"""
URL configuration for app_auth application.
"""
from django.urls import path
from . import views

app_name = 'app_auth'

urlpatterns = [
    # 用户认证相关接口
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('userinfo', views.UserInfoView.as_view(), name='userinfo'),
    path('token/refresh', views.TokenRefreshView.as_view(), name='token_refresh'),
    
    # 用户管理相关接口
    path('password/change', views.PasswordChangeView.as_view(), name='password_change'),
    path('users', views.UserListView.as_view(), name='user_list'),
]
