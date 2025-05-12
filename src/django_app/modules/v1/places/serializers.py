# django_app/modules/v1/places/serializers.py

from rest_framework import serializers

class PlaceSerializer(serializers.ModelSerializer):
    """Standard serializer for Place model"""
