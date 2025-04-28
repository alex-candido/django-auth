# django_app/modules/v1/auth/api.py

from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from .services import AuthService
from .serializers import (
    LoginCredentialsSerializer,
    RegisterCredentialsSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    ChangePasswordSerializer
)

auth_service = AuthService()

class AuthViewSet(viewsets.ModelViewSet):
    """ViewSet for authentication actions."""
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login_credentials(self, request):
        serializer = LoginCredentialsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                result = auth_service.login_credentials(request, serializer.validated_data)
                return Response(result, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register_credentials(self, request):
        serializer = RegisterCredentialsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                result = auth_service.register_credentials(serializer.validated_data)
                return Response(result, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        try:
            auth_service.logout(request, request.data.get("refresh_token"))
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def forgot_password(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                auth_service.forgot_password(serializer.validated_data)
                return Response({"message": "Password reset email sent"}, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({"detail": "Email not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def reset_password(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                auth_service.reset_password(serializer.validated_data)
                return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                auth_service.change_password(request.user, serializer.validated_data)
                return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def access_token(self, request):
        try:
            result = auth_service.create_access_token(request)
            return Response(result, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def refresh_token(self, request):
        try:
            result = auth_service.create_refresh_token(request)
            return Response(result, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def session(self, request):
        result = auth_service.get_session(request.user)
        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def tokens(self, request):
        result = auth_service.get_tokens(request.user)
        return Response(result, status=status.HTTP_200_OK)

