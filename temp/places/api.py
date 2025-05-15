# django_app/modules/v1/places/api.py

from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.gis.geos import Point, WKTReader
from .services import PlaceService
from .serializers import (
    PlaceSerializer, PlaceListSerializer, PlaceCreateUpdateSerializer,
    PlaceGeoFilterSerializer, BoundingBoxSerializer, PolygonSerializer,
    PlaceClusterSerializer
)


place_service = PlaceService()

# find_one, find_all, create_one, create_many, update_one, update_many, remove_one, remove_many, search, semantic_search, filter, find_by_id, find_by_ids, exists_by_id, exists_by_ids, 

# g_near, g_within_box, g_within_polygon, g_along_line, g_wkt, g_distance, g_buffer, g_intersects, g_contains, g_centroid, g_convex_hull, g_cluster, g_k_nearest, g_path_snap

class PlaceViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):
    """ViewSet for place actions."""
    
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'
    
    def get_serializer_class(self):
        """Select appropriate serializer based on action."""
        if self.action in ['create', 'update', 'partial_update']:
            return PlaceCreateUpdateSerializer
        elif self.action == 'list':
            return PlaceListSerializer
        return PlaceSerializer
    
    def get_queryset(self):
        """Get base queryset."""
        # Base implementation - specific filtering is handled by service
        return []
    
    def list(self, request):
        """List all places (with optional filtering)."""
        result = place_service.find_all(request.query_params)
        return Response(result, status=status.HTTP_200_OK)
    
    def retrieve(self, request, uuid=None):
        """Get a place by ID."""
        result = place_service.find_by_id(uuid)
        if result:
            return Response(result, status=status.HTTP_200_OK)
        return Response({"detail": "Place not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        """Create a new place."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = place_service.create_one(serializer.validated_data)
        if result:
            return Response(result, status=status.HTTP_201_CREATED)
        return Response({"detail": "Failed to create place"}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, uuid=None):
        """Update a place."""
        serializer = self.get_serializer(data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        result = place_service.update_one(uuid, serializer.validated_data)
        if result:
            return Response(result, status=status.HTTP_200_OK)
        return Response({"detail": "Place not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def partial_update(self, request, uuid=None):
        """Partially update a place."""
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        result = place_service.update_one(uuid, serializer.validated_data)
        if result:
            return Response(result, status=status.HTTP_200_OK)
        return Response({"detail": "Place not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, uuid=None):
        """Delete a place."""
        result = place_service.remove_one(uuid)
        if result.get('success'):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Place not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # Basic CRUD Operations
    @action(detail=False, methods=['get'])
    def find_one(self, request):
        """Find a single place based on query parameters."""
        result = place_service.find_one(request.query_params)
        if result:
            return Response(result, status=status.HTTP_200_OK)
        return Response({"detail": "Place not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def find_all(self, request):
        """Find all places optionally filtered."""
        result = place_service.find_all(request.query_params)
        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def create_many(self, request):
        """Create multiple places."""
        result = place_service.create_many(request.data)
        return Response(result, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['put'])
    def update_many(self, request):
        """Update multiple places based on filters."""
        filters = request.data.get('filters', {})
        data = request.data.get('data', {})
        result = place_service.update_many(filters, data)
        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['delete'])
    def remove_many(self, request):
        """Delete multiple places based on filters."""
        filters = request.query_params or request.data
        result = place_service.remove_many(filters)
        return Response(result, status=status.HTTP_200_OK)
    
    # Search and Filter operations
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search places by text."""
        query = request.query_params.get('q', '')
        result = place_service.search(query)
        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def semantic_search(self, request):
        """Semantic search places."""
        query = request.query_params.get('q', '')
        result = place_service.semantic_search(query)
        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def filter(self, request):
        """Filter places by parameters."""
        result = place_service.filter(request.query_params)
        return Response(result, status=status.HTTP_200_OK)
    
    # ID-based operations
    @action(detail=False, methods=['get'])
    def find_by_ids(self, request):
        """Find places by multiple IDs."""
        ids = request.query_params.get('ids', '').split(',')
        ids = [id.strip() for id in ids if id.strip()]
        result = place_service.find_by_ids(ids)
        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def exists(self, request, uuid=None):
        """Check if a place exists by ID."""
        result = place_service.exists_by_id(uuid)
        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def exists_many(self, request):
        """Check which place IDs exist."""
        ids = request.query_params.get('ids', '').split(',')
        ids = [id.strip() for id in ids if id.strip()]
        result = place_service.exists_by_ids(ids)
        return Response(result, status=status.HTTP_200_OK)
    
    # Geo operations
    @action(detail=False, methods=['get'])
    def near(self, request):
        """Find places near a point."""
        serializer = PlaceGeoFilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        lat = serializer.validated_data['lat']
        lng = serializer.validated_data['lng']
        distance = serializer.validated_data.get('distance', 10)
        
        result = place_service.g_near(lat, lng, distance)
        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def within_box(self, request):
        """Find places within a bounding box."""
        serializer = BoundingBoxSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        min_lat = serializer.validated_data['min_lat']
        min_lng = serializer.validated_data['min_lng']
        max_lat = serializer.validated_data['max_lat']
        max_lng = serializer.validated_data['max_lng']
        
        result = place_service.g_within_box(min_lat, min_lng, max_lat, max_lng)
        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def within_polygon(self, request):
        """Find places within a polygon."""
        serializer = PolygonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        points = serializer.validated_data['points']
        result = place_service.g_within_polygon(points)
        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def along_line(self, request):
        """Find places along a line."""
        points = request.data.get('points', [])
        distance = request.data.get('distance', 100)  # meters
        result = place_service.g_along_line(points, distance)
        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def wkt(self, request):
        """Find places based on WKT geometry."""
        wkt = request.data.get('wkt', '')
        operation = request.data.get('operation', 'intersects')
        result = place_service.g_wkt(wkt, operation)
        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def distance(self, request):
        """Get places with distance from a point."""
        serializer = PlaceGeoFilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        lat = serializer.validated_data['lat']
        lng = serializer.validated_data['lng']
        
        result = place_service.g_distance(lat, lng)
        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def buffer(self, request):
        """Find places within a buffer around a point."""
        lat = float(request.query_params.get('lat', 0))
        lng = float(request.query_params.get('lng', 0))
        radius = float(request.query_params.get('radius', 1000))  # meters
        
        result = place_service.g_buffer(lat, lng, radius)
        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def centroid(self, request):
        """Get centroids of places."""
        result = place_service.g_centroid()
        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def convex_hull(self, request):
        """Get convex hull of places."""
        result = place_service.g_convex_hull()
        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def cluster(self, request):
        """Cluster places."""
        serializer = PlaceClusterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        grid_size = serializer.validated_data.get('grid_size', 0.01)
        result = place_service.g_cluster(grid_size)
        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def k_nearest(self, request):
        """Find k nearest places to a point."""
        lat = float(request.query_params.get('lat', 0))
        lng = float(request.query_params.get('lng', 0))
        k = int(request.query_params.get('k', 5))
        
        result = place_service.g_k_nearest(lat, lng, k)
        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def path_snap(self, request):
        """Snap places to a path."""
        points = request.data.get('points', [])
        result = place_service.g_path_snap(points)
        return Response(result, status=status.HTTP_200_OK)