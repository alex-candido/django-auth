# django_app/modules/v1/places/serializers.py

from rest_framework import serializers
from django.contrib.gis.geos import Point
from .models import Place

class PlaceSerializer(serializers.ModelSerializer):
    """Serializer for the Place model.
    
    This serializer handles the conversion between Place model instances and JSON,
    including proper handling of geographic coordinates.
    """
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
    
    class Meta:
        model = Place
        fields = ['id', 'name', 'description', 'address', 'latitude', 'longitude', 'created_at', 'updated_at', 'created_by']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Create a new Place instance with proper handling of geographic coordinates."""
        latitude = validated_data.pop('latitude', 0.0)
        longitude = validated_data.pop('longitude', 0.0)
        
        # Create a Point object for the location
        validated_data['location'] = Point(longitude, latitude)
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Update a Place instance with proper handling of geographic coordinates."""
        if 'latitude' in validated_data or 'longitude' in validated_data:
            latitude = validated_data.pop('latitude', instance.latitude)
            longitude = validated_data.pop('longitude', instance.longitude)
            instance.location = Point(longitude, latitude)
        
        return super().update(instance, validated_data)