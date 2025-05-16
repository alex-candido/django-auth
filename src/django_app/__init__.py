# django_app/__init__.py

from .container import Container
from . import settings

container = Container()
container.config.from_dict(settings.__dict__)
