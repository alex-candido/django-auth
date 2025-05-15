# django_app/modules/v1/places/urls.py

from rest_framework.routers import DefaultRouter

from .api import PlaceViewSet

router = DefaultRouter()
router.register(r'', PlaceViewSet,  basename='places')

urlpatterns = router.urls
