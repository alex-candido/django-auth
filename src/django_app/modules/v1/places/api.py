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

class PlaceViewSet(viewsets.GenericViewSet):
    pass
    
 