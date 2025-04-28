# django_app/modules/v1/auth/apps.py

from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_app.modules.v1.auth'
    label = 'custom_auth'
    verbose_name = 'Auth'
