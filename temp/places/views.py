# django_app/modules/v1/places/views.py

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.contrib.gis.db.models.functions import Distance as DistanceFunction
from .models import Place
from .serializers import PlaceSerializer

class PlaceViewSet(viewsets.ModelViewSet):
    """ViewSet for the Place model.
    
    Provides CRUD operations and additional spatial queries for places.
    """
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        """Set the created_by field to the current user when creating a place."""
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """Find places near a specified location.
        
        Query parameters:
        - lat: Latitude of the center point
        - lng: Longitude of the center point
        - radius: Search radius in kilometers (default: 10)
        """
        try:
            lat = float(request.query_params.get('lat', 0))
            lng = float(request.query_params.get('lng', 0))
            radius = float(request.query_params.get('radius', 10))
            
            # Create a point from the provided coordinates
            point = Point(lng, lat, srid=4326)
            
            # Query places within the radius
            places = Place.objects.filter(
                location__distance_lte=(point, Distance(km=radius))
            ).annotate(
                distance=DistanceFunction('location', point)
            ).order_by('distance')
            
            serializer = self.get_serializer(places, many=True)
            return Response(serializer.data)
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid parameters. Please provide valid lat, lng, and radius values."},
                status=400
            )