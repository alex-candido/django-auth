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
    def find_one(self, params):
        """Find a single place based on filter parameters."""
        try:
            filters = self._build_filters(params)
            return Place.objects.filter(**filters).first()
        except Exception as e:
            print(f"Error in find_one: {str(e)}")
            return None

    def find_all(self, params=None):
        """Find all places, optionally filtered by parameters."""
        try:
            if params:
                filters = self._build_filters(params)
                return Place.objects.filter(**filters)
            return Place.objects.all()
        except Exception as e:
            print(f"Error in find_all: {str(e)}")
            return Place.objects.none()

    def create_one(self, data):
        """Create a new place."""
        try:
            # Generate slug if not provided
            if 'slug' not in data or not data['slug']:
                data['slug'] = slugify(data['name'])
                
                # Ensure slug is unique by appending random string if needed
                if Place.objects.filter(slug=data['slug']).exists():
                    data['slug'] = f"{data['slug']}-{str(uuid.uuid4())[:8]}"
            
            # Handle location data
            if 'latitude' in data and 'longitude' in data:
                lat = float(data.pop('latitude', 0))
                lng = float(data.pop('longitude', 0))
                data['location'] = Point(lng, lat, srid=4326)
            
            place = Place.objects.create(**data)
            return place
        except Exception as e:
            print(f"Error in create_one: {str(e)}")
            return None

    def create_many(self, data_list):
        """Create multiple places."""
        created_places = []
        for data in data_list:
            place = self.create_one(data)
            if place:
                created_places.append(place)
        return created_places

    def update_one(self, place_id, data):
        """Update a place by ID."""
        try:
            place = Place.objects.get(uuid=place_id)
            
            # Handle location separately if provided
            if 'latitude' in data and 'longitude' in data:
                lat = float(data.pop('latitude', 0))
                lng = float(data.pop('longitude', 0))
                place.location = Point(lng, lat, srid=4326)
            
            # Update other fields
            for key, value in data.items():
                if hasattr(place, key):
                    setattr(place, key, value)
            
            place.save()
            return place
        except Place.DoesNotExist:
            return None
        except Exception as e:
            print(f"Error in update_one: {str(e)}")
            return None

    def update_many(self, filters, data):
        """Update multiple places based on filters."""
        try:
            filter_dict = self._build_filters(filters)
            places = Place.objects.filter(**filter_dict)
            updated_count = places.update(**data)
            return updated_count
        except Exception as e:
            print(f"Error in update_many: {str(e)}")
            return 0

    def remove_one(self, place_id):
        """Delete a place by ID."""
        try:
            place = Place.objects.get(uuid=place_id)
            place.delete()
            return True
        except Place.DoesNotExist:
            return False
        except Exception as e:
            print(f"Error in remove_one: {str(e)}")
            return False

    def remove_many(self, filters):
        """Delete multiple places based on filters."""
        try:
            filter_dict = self._build_filters(filters)
            deleted_count, _ = Place.objects.filter(**filter_dict).delete()
            return deleted_count
        except Exception as e:
            print(f"Error in remove_many: {str(e)}")
            return 0

    def search(self, query):
        """Search places by name, description, address, etc."""
        try:
            return Place.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(address__icontains=query) |
                Q(city__icontains=query) |
                Q(state__icontains=query) |
                Q(country__icontains=query)
            )
        except Exception as e:
            print(f"Error in search: {str(e)}")
            return Place.objects.none()

    def filter(self, params):
        """Filter places based on multiple parameters."""
        try:
            filters = self._build_filters(params)
            return Place.objects.filter(**filters)
        except Exception as e:
            print(f"Error in filter: {str(e)}")
            return Place.objects.none()

    def find_by_id(self, place_id):
        """Find a place by ID."""
        try:
            return Place.objects.get(uuid=place_id)
        except Place.DoesNotExist:
            return None
        except Exception as e:
            print(f"Error in find_by_id: {str(e)}")
            return None

    def find_by_ids(self, place_ids):
        """Find places by multiple IDs."""
        try:
            return Place.objects.filter(uuid__in=place_ids)
        except Exception as e:
            print(f"Error in find_by_ids: {str(e)}")
            return Place.objects.none()

    def exists_by_id(self, place_id):
        """Check if a place exists by ID."""
        return Place.objects.filter(uuid=place_id).exists()

    def exists_by_ids(self, place_ids):
        """Check which place IDs exist."""
        existing_ids = Place.objects.filter(uuid__in=place_ids).values_list('uuid', flat=True)
        return list(existing_ids)

    # Geo-specific methods
    def g_near(self, lat, lng, distance_km=10):
        """Find places near a point."""
        try:
            point = Point(float(lng), float(lat), srid=4326)
            return Place.objects.filter(
                location__distance_lte=(point, D(km=distance_km))
            ).annotate(
                distance=Distance('location', point)
            ).order_by('distance')
        except Exception as e:
            print(f"Error in g_near: {str(e)}")
            return Place.objects.none()

    def g_within_box(self, min_lat, min_lng, max_lat, max_lng):
        """Find places within a bounding box."""
        try:
            bbox = Polygon.from_bbox((float(min_lng), float(min_lat), float(max_lng), float(max_lat)))
            return Place.objects.filter(location__within=bbox)
        except Exception as e:
            print(f"Error in g_within_box: {str(e)}")
            return Place.objects.none()

    def g_within_polygon(self, points):
        """Find places within a polygon."""
        try:
            polygon = Polygon(points, srid=4326)
            return Place.objects.filter(location__within=polygon)
        except Exception as e:
            print(f"Error in g_within_polygon: {str(e)}")
            return Place.objects.none()

    def g_along_line(self, points, distance_m=100):
        """Find places along a line within a certain distance."""
        try:
            line = LineString(points, srid=4326)
            return Place.objects.filter(
                location__distance_lte=(line, D(m=distance_m))
            )
        except Exception as e:
            print(f"Error in g_along_line: {str(e)}")
            return Place.objects.none()

    def g_wkt(self, wkt, operation='intersects'):
        """Find places based on WKT geometry and operation."""
        try:
            reader = WKTReader()
            geom = reader.read(wkt)
            
            if operation == 'intersects':
                return Place.objects.filter(location__intersects=geom)
            elif operation == 'within':
                return Place.objects.filter(location__within=geom)
            elif operation == 'contains':
                return Place.objects.filter(location__contains=geom)
            elif operation == 'dwithin':
                # Default distance 100m
                return Place.objects.filter(location__dwithin=(geom, 100))
            else:
                raise ValueError(f"Unsupported operation: {operation}")
        except Exception as e:
            print(f"Error in g_wkt: {str(e)}")
            return Place.objects.none()

    def g_distance(self, lat, lng):
        """Find places with distance from a point."""
        try:
            point = Point(float(lng), float(lat), srid=4326)
            return Place.objects.annotate(
                distance=Distance('location', point)
            ).order_by('distance')
        except Exception as e:
            print(f"Error in g_distance: {str(e)}")
            return Place.objects.none()

    def g_buffer(self, lat, lng, radius_m=1000):
        """Find places within a buffer around a point."""
        try:
            point = Point(float(lng), float(lat), srid=4326)
            return Place.objects.filter(
                location__dwithin=(point, D(m=radius_m))
            )
        except Exception as e:
            print(f"Error in g_buffer: {str(e)}")
            return Place.objects.none()

    def g_intersects(self, geom):
        """Find places that intersect with a geometry."""
        try:
            return Place.objects.filter(location__intersects=geom)
        except Exception as e:
            print(f"Error in g_intersects: {str(e)}")
            return Place.objects.none()

    def g_contains(self, geom):
        """Find places that contain a geometry."""
        try:
            return Place.objects.filter(location__contains=geom)
        except Exception as e:
            print(f"Error in g_contains: {str(e)}")
            return Place.objects.none()

    def g_centroid(self):
        """Get centroids of places."""
        try:
            return Place.objects.annotate(centroid=Centroid('location'))
        except Exception as e:
            print(f"Error in g_centroid: {str(e)}")
            return Place.objects.none()

    def g_convex_hull(self):
        """Get convex hull of places."""
        try:
            return Place.objects.annotate(convex_hull=ConvexHull('location'))
        except Exception as e:
            print(f"Error in g_convex_hull: {str(e)}")
            return Place.objects.none()

    def g_cluster(self, grid_size=10):
        """Cluster places by grid."""
        # Basic implementation - could be improved with proper spatial clustering
        try:
            return Place.objects.extra(
                select={'cluster': f"ST_SnapToGrid(location, {grid_size}, {grid_size})"}
            ).values('cluster').annotate(count=Count('uuid')).order_by('-count')
        except Exception as e:
            print(f"Error in g_cluster: {str(e)}")
            return []

    def g_k_nearest(self, lat, lng, k=5):
        """Find k nearest places to a point."""
        try:
            point = Point(float(lng), float(lat), srid=4326)
            return Place.objects.annotate(
                distance=Distance('location', point)
            ).order_by('distance')[:k]
        except Exception as e:
            print(f"Error in g_k_nearest: {str(e)}")
            return Place.objects.none()

    def g_path_snap(self, points):
        """Snap places to a path (nearest places to each point on a path)."""
        try:
            result = []
            for point_coords in points:
                lng, lat = point_coords
                point = Point(lng, lat, srid=4326)
                nearest = Place.objects.annotate(
                    distance=Distance('location', point)
                ).order_by('distance').first()
                if nearest:
                    result.append(nearest)
            return result
        except Exception as e:
            print(f"Error in g_path_snap: {str(e)}")
            return []

    def _build_filters(self, params):
        """Build Django ORM filters from request parameters."""
        filters = {}
        
        # Handle exact field matches
        for field in ['name', 'slug', 'city', 'state', 'country', 'postal_code', 'type', 'status']:
            if field in params:
                filters[field] = params[field]
        
        # Handle partial text matches
        for field in ['name__icontains', 'description__icontains', 'address__icontains', 
                      'city__icontains', 'state__icontains', 'country__icontains']:
            base_field = field.split('__')[0]
            if base_field in params:
                filters[field] = params[base_field]
        
        return filters