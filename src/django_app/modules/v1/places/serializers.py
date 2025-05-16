# django_app/modules/v1/places/serializers.py

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.geos import Point
from .models import Place

class PlaceIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class PlaceCreateRequestSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True, required=False)
    longitude = serializers.FloatField(write_only=True, required=False)
    
    class Meta:
        model = Place
        fields = ('name', 'slug', 'description', 'address', 'city', 'state', 
                  'country', 'postal_code', 'website', 'phone', 'email', 
                  'type', 'status', 'latitude', 'longitude')
    
    def validate(self, data):
        """Validate that latitude and longitude are provided together."""
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if (latitude is not None and longitude is None) or (latitude is None and longitude is not None):
            raise serializers.ValidationError("Both latitude and longitude must be provided together")
        
        return data

class PlaceUpdateRequestSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    latitude = serializers.FloatField(write_only=True, required=False)
    longitude = serializers.FloatField(write_only=True, required=False)
    
    class Meta:
        model = Place
        fields = ('id', 'name', 'slug', 'description', 'address', 'city', 'state', 
                  'country', 'postal_code', 'website', 'phone', 'email', 
                  'type', 'status', 'latitude', 'longitude')
    
    def validate(self, data):
        """Validate that latitude and longitude are provided together."""
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if (latitude is not None and longitude is None) or (latitude is None and longitude is not None):
            raise serializers.ValidationError("Both latitude and longitude must be provided together")
        
        return data

class PaginationRequestSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, default=1)
    per_page = serializers.IntegerField(required=False, default=10)
    sort = serializers.CharField(required=False, default='id')
    sort_dir = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='asc')

class PlaceSearchRequestSerializer(PaginationRequestSerializer):
    query = serializers.CharField()
    field = serializers.ChoiceField(choices=['name', 'description', 'address', 'city', 'state', 'country'])

class PlaceFilterRequestSerializer(PaginationRequestSerializer):
    uuid = serializers.UUIDField(required=False)
    name = serializers.CharField(required=False)
    slug = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    type = serializers.IntegerField(required=False)
    status = serializers.IntegerField(required=False)

class PlaceResponseSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    
    class Meta:
        model = Place
        fields = ('id', 'uuid', 'name', 'slug', 'description', 'address', 'city', 'state', 
                  'country', 'postal_code', 'website', 'phone', 'email', 
                  'type', 'type_display', 'status', 'status_display',
                  'created_at', 'updated_at', 'latitude', 'longitude')
    
    def get_latitude(self, obj):
        return obj.latitude()
    
    def get_longitude(self, obj):
        return obj.longitude()

class PlaceCreateResponseSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    
    class Meta:
        model = Place
        fields = ('id', 'uuid', 'name', 'slug', 'type', 'type_display', 'status', 'status_display', 'latitude', 'longitude')
    
    def get_latitude(self, obj):
        return obj.latitude()
    
    def get_longitude(self, obj):
        return obj.longitude()

class PlaceExistsResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    exists = serializers.BooleanField()

class PaginationResponseSerializer(serializers.Serializer):
    items = serializers.ListField()
    total = serializers.IntegerField()
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    last_page = serializers.IntegerField()

class PlaceSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    
    class Meta:
        model = Place
        fields = ('id', 'uuid', 'name', 'slug', 'description', 'address', 'city', 'state', 
                  'country', 'postal_code', 'website', 'phone', 'email', 
                  'type', 'type_display', 'status', 'status_display',
                  'created_at', 'updated_at', 'latitude', 'longitude')
        read_only_fields = ('id', 'uuid', 'created_at', 'updated_at')
    
    def get_latitude(self, obj):
        return obj.latitude()
    
    def get_longitude(self, obj):
        return obj.longitude()

# Geo-specific serializers
class NearbyPlacesRequestSerializer(PaginationRequestSerializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    radius = serializers.FloatField(required=False, default=5000)  # Default 5km radius

class WithinBoxRequestSerializer(PaginationRequestSerializer):
    min_lat = serializers.FloatField()
    min_lng = serializers.FloatField()
    max_lat = serializers.FloatField()
    max_lng = serializers.FloatField()

class PlaceGeoFeatureSerializer(GeoFeatureModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    distance = serializers.SerializerMethodField()
    
    class Meta:
        model = Place
        geo_field = "location"
        fields = ('id', 'uuid', 'name', 'slug', 'description', 'address', 'city', 'state', 
                  'country', 'postal_code', 'website', 'phone', 'email', 
                  'type', 'type_display', 'status', 'status_display',
                  'created_at', 'updated_at', 'distance')
    
    def get_distance(self, obj):
        """Get distance if it was annotated by the query."""
        if hasattr(obj, 'distance'):
            # Convert to meters
            return getattr(obj.distance, 'm', None)
        return None