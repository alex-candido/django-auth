# django_app/modules/v1/users/urls.py

from rest_framework.routers import DefaultRouter

from .api import UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = router.urls