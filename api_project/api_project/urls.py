"""
URL configuration for api_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 用户认证模块
    path('api/auth/', include('app_auth.urls')),
    
    # 业务数据模块
    path('api/', include('app_web.urls')),
]
