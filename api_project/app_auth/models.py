from django.contrib.auth.models import AbstractUser

import uuid
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    # 基本信息字段
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True)
    real_name = models.CharField(max_length=100, blank=True, null=True)
    gender_choices = (
        ('男', '男'),
        ('女', '女')
    )
    gender = models.CharField(max_length=10, choices=gender_choices, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    # 认证与安全字段
    password = models.CharField(max_length=128)
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    salt = models.CharField(max_length=16, blank=True, null=True)
    login_count = models.PositiveIntegerField(default=0)
    last_login_time = models.DateTimeField(blank=True, null=True)

    # 权限与角色字段
    role_choices = (
        ('admin', '管理员'),
        ('normal', '普通用户'),
        ('vip', '高级用户')
    )
    user_role = models.CharField(max_length=20, choices=role_choices, default='normal')
    # 假设权限用字符串存储类似 'create,read,update'，实际可通过多对多关系关联权限表
    permission_flags = models.CharField(max_length=255, blank=True)

    # 系统状态与扩展字段
    is_active = models.BooleanField(default=True)
    registration_time = models.DateTimeField(default=timezone.now)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    signature = models.CharField(max_length=500, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.username

    class Meta:
        db_table = "app_auth_user"
        verbose_name = "用户"
        verbose_name_plural = "用户"
