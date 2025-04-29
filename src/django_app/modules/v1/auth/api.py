# django_app/modules/v1/auth/api.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from dj_rest_auth.views import LoginView, LogoutView, PasswordChangeView, UserDetailsView
from django_rest_passwordreset.views import ResetPasswordRequestToken, ResetPasswordConfirm
from dj_rest_auth.registration.views import (
    RegisterView,
    VerifyEmailView,
    ResendEmailVerificationView
)

class AuthViewSet(viewsets.ViewSet):  # Note: ModelViewSet não é necessário
    permission_classes = [AllowAny]

    def _dispatch_view(self, view_cls, request: Request):
        """Utilitário interno para invocar uma view baseada em classe corretamente."""
        view = view_cls.as_view()
        return view(request._request)  # Usa o HttpRequest internamente de forma segura

    @action(detail=False, methods=['post'])
    def login_credentials(self, request):
        return self._dispatch_view(LoginView, request)

    @action(detail=False, methods=['post'])
    def register_credentials(self, request):
        return self._dispatch_view(RegisterView, request)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        return self._dispatch_view(LogoutView, request)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        return self._dispatch_view(PasswordChangeView, request)

    @action(detail=False, methods=['post'])
    def forgot_password(self, request):
        return self._dispatch_view(ResetPasswordRequestToken, request)

    @action(detail=False, methods=['post'])
    def resend_verification_email(self, request):
        return self._dispatch_view(ResendEmailVerificationView, request)

    @action(detail=False, methods=['post'])
    def verify_email(self, request):
        return self._dispatch_view(VerifyEmailView, request)

    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        return self._dispatch_view(ResetPasswordConfirm, request)

    @action(detail=False, methods=['post'])
    def access_token(self, request):
        return self._dispatch_view(TokenObtainPairView, request)

    @action(detail=False, methods=['post'])
    def refresh_token(self, request):
        return self._dispatch_view(TokenRefreshView, request)

    @action(detail=False, methods=['post'])
    def verify_token(self, request):
        return self._dispatch_view(TokenVerifyView, request)

    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[IsAuthenticated])
    def user(self, request):
        return self._dispatch_view(UserDetailsView, request)
