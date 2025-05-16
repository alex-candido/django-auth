# django_app/modules/v1/users/apps.py

from django.apps import AppConfig
from dependency_injector import providers

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_app.modules.v1.users'
    label = 'users'
    verbose_name = 'Users'
    container = None

    def ready(self):
        from .container import UserContainer
        self.container = UserContainer()