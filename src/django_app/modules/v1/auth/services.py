# django_app/modules/v1/auth/services.py

from django.contrib.auth import authenticate, login, logout
from django_app.modules.v1.users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from .repositories import AuthRepository
from .models import TokenBlacklist

class AuthService:
    def __init__(self):
        self.repository = AuthRepository()

    def login_credentials(self, request, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            }
        raise ValueError('Invalid credentials')

    def register_credentials(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise ValueError('Username already exists')
        if User.objects.filter(email=data['email']).exists():
            raise ValueError('Email already exists')
        
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        refresh = RefreshToken.for_user(user)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }

    def logout(self, request, refresh_token):
        if not refresh_token:
            raise ValueError("Refresh token is required for logout")
        TokenBlacklist.objects.create(
            token=refresh_token,
            expires_at=timezone.now() + timezone.timedelta(days=1)
        )
        logout(request)

    def is_token_blacklisted(self, token):
        return TokenBlacklist.objects.filter(
            token=token,
            expires_at__gt=timezone.now()
        ).exists()

    def forgot_password(self, data):
        user = self.repository.find_by_email(data['email'])
        if not user:
            raise ValueError("Email not found")
        # Generate and send password reset token
        token = self.repository.create_password_reset_token(user)
        self.repository.send_password_reset_email(user.email, token)

    def reset_password(self, data):
        user = self.repository.verify_password_reset_token(data['token'])
        if not user:
            raise ValueError('Invalid or expired token')
        user.set_password(data['new_password'])
        user.save()

    def change_password(self, user, data):
        if not user.check_password(data['current_password']):
            raise ValueError('Current password is incorrect')
        user.set_password(data['new_password'])
        user.save()

    def create_access_token(self, request):
        refresh_token = request.data.get('refresh_token')
        if self.is_token_blacklisted(refresh_token):
            raise ValueError('Token has been blacklisted')
        refresh = RefreshToken(refresh_token)
        return {
            'access_token': str(refresh.access_token)
        }

    def create_refresh_token(self, request):
        user = authenticate(
            username=request.data.get('username'),
            password=request.data.get('password')
        )
        if not user:
            raise ValueError('Invalid credentials')
        refresh = RefreshToken.for_user(user)
        return {
            'refresh_token': str(refresh)
        }

    def get_session(self, user):
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active
        }

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }
