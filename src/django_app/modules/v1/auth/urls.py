# django_app/modules/v1/auth/urls.py

from rest_framework.routers import DefaultRouter

from .api import AuthViewSet

router = DefaultRouter()
router.register(r'', AuthViewSet, basename='auth')

urlpatterns = router.urls