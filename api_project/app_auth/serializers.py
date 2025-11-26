from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
import uuid
import secrets

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    """登录序列化器"""
    username = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(max_length=128, required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('用户名或密码错误')
            if not user.is_active:
                raise serializers.ValidationError('用户账户已被禁用')
            
            # 更新登录信息
            user.login_count += 1
            user.last_login_time = timezone.now()
            user.save(update_fields=['login_count', 'last_login_time'])
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('用户名和密码都是必填项')

    def create(self, validated_data):
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return {
            'user': user,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class RegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(write_only=True, min_length=8, 
                                   error_messages={'min_length': '密码至少8位'})
    password_confirm = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True, error_messages={'required': '邮箱是必填项'})

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'email', 'real_name', 
                 'gender', 'date_of_birth', 'phone_number']

    def validate_username(self, value):
        """验证用户名唯一性"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('用户名已存在')
        if len(value) < 3:
            raise serializers.ValidationError('用户名至少3位')
        return value

    def validate_email(self, value):
        """验证邮箱唯一性"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('邮箱已被注册')
        return value

    def validate_phone_number(self, value):
        """验证手机号格式"""
        if value and not value.isdigit():
            raise serializers.ValidationError('手机号必须是数字')
        if value and len(value) != 11:
            raise serializers.ValidationError('手机号必须是11位')
        return value

    def validate(self, attrs):
        """验证密码一致性"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': '两次输入的密码不一致'})
        
        # 密码复杂度检查
        password = attrs['password']
        if not any(c.isdigit() for c in password):
            raise serializers.ValidationError({'password': '密码必须包含数字'})
        if not any(c.isalpha() for c in password):
            raise serializers.ValidationError({'password': '密码必须包含字母'})
        
        return attrs

    def create(self, validated_data):
        """创建用户"""
        validated_data.pop('password_confirm')
        
        # 生成salt
        salt = secrets.token_hex(8)
        validated_data['salt'] = salt
        
        # 创建用户
        user = User.objects.create_user(**validated_data)
        
        return user


class UserSerializer(serializers.ModelSerializer):
    """用户信息序列化器"""
    user_role_display = serializers.CharField(source='get_user_role_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'real_name', 'email', 'gender', 'gender_display',
                 'date_of_birth', 'phone_number', 'avatar', 'signature', 'user_role',
                 'user_role_display', 'login_count', 'last_login_time', 'registration_time',
                 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'login_count', 'last_login_time', 'registration_time',
                           'created_at', 'updated_at']


class UserProfileSerializer(serializers.ModelSerializer):
    """用户资料更新序列化器"""
    
    class Meta:
        model = User
        fields = ['real_name', 'gender', 'date_of_birth', 'phone_number', 
                 'avatar', 'signature', 'remark']

    def validate_phone_number(self, value):
        """验证手机号格式"""
        if value and not value.isdigit():
            raise serializers.ValidationError('手机号必须是数字')
        if value and len(value) != 11:
            raise serializers.ValidationError('手机号必须是11位')
        return value


class PasswordChangeSerializer(serializers.Serializer):
    """修改密码序列化器"""
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        """验证旧密码"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('旧密码错误')
        return value

    def validate(self, attrs):
        """验证新密码一致性"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({'new_password_confirm': '两次输入的新密码不一致'})
        
        # 密码复杂度检查
        password = attrs['new_password']
        if not any(c.isdigit() for c in password):
            raise serializers.ValidationError({'new_password': '密码必须包含数字'})
        if not any(c.isalpha() for c in password):
            raise serializers.ValidationError({'new_password': '密码必须包含字母'})
        
        return attrs

    def save(self):
        """保存新密码"""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class TokenRefreshSerializer(serializers.Serializer):
    """Token刷新序列化器"""
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = attrs['refresh']
        try:
            token = RefreshToken(refresh)
            token.check_blacklist()
            
            return {
                'access': str(token.access_token),
            }
        except Exception as e:
            raise serializers.ValidationError('Token无效或已过期')