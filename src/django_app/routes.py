# django_app/routes.py

from django.urls import path, include

urlpatterns = [
    path('auth/', include('django_app.modules.v1.auth.urls')),
    path('users/', include('django_app.modules.v1.users.urls')),
]