# django_app/container.py

from dependency_injector import containers, providers

from django_app.modules.v1.users.container import UserContainer

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    users = providers.Container(UserContainer, config=config)
