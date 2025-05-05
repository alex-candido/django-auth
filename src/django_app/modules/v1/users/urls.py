# django_app/modules/v1/users/urls.py

from rest_framework.routers import DefaultRouter

from .api import UserApiSet

router = DefaultRouter()
router.register(r'', UserApiSet, basename='users')

urlpatterns = router.urls