# django_app/modules/v1/places/serializers.py

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.geos import Point
from .models import Place

# PlaceSerializer, PlaceListSerializer, PlaceCreateUpdateSerializer, PlaceGeoFilterSerializer, PlaceClusterSerializer, BoundingBoxSerializer, PolygonSerializer

class PlaceListSerializer(serializers.ModelSerializer):
    """Serializer for list view (non-geo format)."""
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    
    class Meta:
        model = Place
        fields = ('uuid', 'name', 'slug', 'address', 'city', 'state', 'country', 
                  'type', 'type_display', 'status', 'status_display', 
                  'latitude', 'longitude', 'created_at')
    
    def get_latitude(self, obj):
        return obj.latitude()
    
    def get_longitude(self, obj):
        return obj.longitude()


class PlaceSerializer(GeoFeatureModelSerializer):
    """Full Place serializer with geo-features."""
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    
    class Meta:
        model = Place
        geo_field = "location"
        fields = ('uuid', 'name', 'slug', 'description', 'address', 'city', 'state', 
                  'country', 'postal_code', 'website', 'phone', 'email', 
                  'type', 'type_display', 'status', 'status_display',
                  'created_at', 'updated_at', 'latitude', 'longitude', 'distance')
    
    def get_latitude(self, obj):
        return obj.latitude()
    
    def get_longitude(self, obj):
        return obj.longitude()
    
    def get_distance(self, obj):
        """Get distance if it was annotated by the query."""
        if hasattr(obj, 'distance'):
            # Convert to meters
            return getattr(obj.distance, 'm', None)
        return None


class PlaceCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for create/update operations."""
    latitude = serializers.FloatField(write_only=True, required=False)
    longitude = serializers.FloatField(write_only=True, required=False)
    
    class Meta:
        model = Place
        fields = ('uuid', 'name', 'slug', 'description', 'address', 'city', 'state', 
                  'country', 'postal_code', 'website', 'phone', 'email', 
                  'type', 'status', 'latitude', 'longitude')
        read_only_fields = ('uuid',)
    
    def validate(self, data):
        """Validate that latitude and longitude are provided together."""
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if (latitude is not None and longitude is None) or (latitude is None and longitude is not None):
            raise serializers.ValidationError("Both latitude and longitude must be provided together")
        
        return data
    
    def create(self, validated_data):
        """Custom create to handle location point."""
        latitude = validated_data.pop('latitude', None)
        longitude = validated_data.pop('longitude', None)
        
        place = Place(**validated_data)
        
        if latitude is not None and longitude is not None:
            place.location = Point(longitude, latitude, srid=4326)
        
        place.save()
        return place
    
    def update(self, instance, validated_data):
        """Custom update to handle location point."""
        latitude = validated_data.pop('latitude', None)
        longitude = validated_data.pop('longitude', None)
        
        # Update standard fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update location if provided
        if latitude is not None and longitude is not None:
            instance.location = Point(longitude, latitude, srid=4326)
        
        instance.save()
        return instance


class PlaceGeoFilterSerializer(serializers.Serializer):
    """Serializer for geo filter parameters."""
    lat = serializers.FloatField(required=True)
    lng = serializers.FloatField(required=True)
    distance = serializers.FloatField(required=False, default=10)
    
    def validate_distance(self, value):
        if value <= 0:
            raise serializers.ValidationError("Distance must be positive")
        return value


class PlaceClusterSerializer(serializers.Serializer):
    """Serializer for clustering parameters."""
    grid_size = serializers.FloatField(required=False, default=0.01)
    
    def validate_grid_size(self, value):
        if value <= 0:
            raise serializers.ValidationError("Grid size must be positive")
        return value


class BoundingBoxSerializer(serializers.Serializer):
    """Serializer for bounding box parameters."""
    min_lat = serializers.FloatField(required=True)
    min_lng = serializers.FloatField(required=True)
    max_lat = serializers.FloatField(required=True)
    max_lng = serializers.FloatField(required=True)
    
    def validate(self, data):
        if data['min_lat'] >= data['max_lat']:
            raise serializers.ValidationError("min_lat must be less than max_lat")
        if data['min_lng'] >= data['max_lng']:
            raise serializers.ValidationError("min_lng must be less than max_lng")
        return data


class PolygonSerializer(serializers.Serializer):
    """Serializer for polygon parameters."""
    points = serializers.ListField(
        child=serializers.ListField(
            child=serializers.FloatField(),
            min_length=2,
            max_length=2
        ),
        min_length=3
    )
    
    def validate_points(self, value):
        if value[0] != value[-1]:
            # Add the first point to close the polygon
            value.append(value[0])
        return value