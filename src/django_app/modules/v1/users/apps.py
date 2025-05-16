# django_app/modules/v1/users/apps.py

from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_app.modules.v1.users'
    label = 'users'
    verbose_name = 'Users'

    def ready(self):
        from django_app import container
        container.users().wire(modules=[
            'django_app.modules.v1.users.api',
        ])