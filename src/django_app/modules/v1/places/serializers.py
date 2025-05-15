# django_app/modules/v1/places/serializers.py

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.geos import Point
from .models import Place

# PlaceSerializer, PlaceListSerializer, PlaceCreateUpdateSerializer, PlaceGeoFilterSerializer, PlaceClusterSerializer, BoundingBoxSerializer, PolygonSerializer

class PlaceListSerializer(serializers.ModelSerializer):
    pass