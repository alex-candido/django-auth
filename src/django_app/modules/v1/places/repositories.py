# django_app/modules/v1/places/repositories.py

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point, Polygon, LineString, WKTReader
from django.contrib.gis.measure import D
from django.db.models import Q
from django.contrib.gis.db.models.functions import Centroid, ConvexHull
from django.db.models.aggregates import Count
from django.utils.text import slugify
import uuid

from .models import Place

# find_one, find_all, create_one, create_many, update_one, update_many, remove_one, remove_many, search, semantic_search, filter, find_by_id, find_by_ids, exists_by_id, exists_by_ids, 

# g_near, g_within_box, g_within_polygon, g_along_line, g_wkt, g_distance, g_buffer, g_intersects, g_contains, g_centroid, g_convex_hull, g_cluster, g_k_nearest, g_path_snap

class PlaceRepository:
    pass