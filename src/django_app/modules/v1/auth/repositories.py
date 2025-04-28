# django_app/modules/v1/auth/repositories.py

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django_app.modules.v1.users.models import User

class AuthRepository:
    def find_by_email(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def create_password_reset_token(self, user):
        return default_token_generator.make_token(user)

    def verify_password_reset_token(self, token):
        try:
            user = User.objects.get(pk=token.split('-')[0])
            if default_token_generator.check_token(user, token):
                return user
            return None
        except (TypeError, ValueError, User.DoesNotExist):
            return None

    def send_password_reset_email(self, email, token):
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        send_mail(
            subject='Password Reset Request',
            message=f'Click the following link to reset your password: {reset_url}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )