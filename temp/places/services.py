# django_app/modules/v1/places/services.py

from .repositories import PlaceRepository
from .serializers import PlaceSerializer

# find_one, find_all, create_one, create_many, update_one, update_many, remove_one, remove_many, search, semantic_search, filter, find_by_id, find_by_ids, exists_by_id, exists_by_ids, 

# g_near, g_within_box, g_within_polygon, g_along_line, g_wkt, g_distance, g_buffer, g_intersects, g_contains, g_centroid, g_convex_hull, g_cluster, g_k_nearest, g_path_snap

class PlaceService:
    def __init__(self):
        self.repository = PlaceRepository()
    
    def find_one(self, params):
        """Find a single place by parameters."""
        place = self.repository.find_one(params)
        if place:
            return PlaceSerializer(place).data
        return None

    def find_all(self, params=None):
        """Find all places, optionally filtered."""
        places = self.repository.find_all(params)
        return PlaceSerializer(places, many=True).data

    def create_one(self, data):
        """Create a new place."""
        place = self.repository.create_one(data)
        if place:
            return PlaceSerializer(place).data
        return None

    def create_many(self, data_list):
        """Create multiple places."""
        places = self.repository.create_many(data_list)
        return PlaceSerializer(places, many=True).data

    def update_one(self, place_id, data):
        """Update a place by ID."""
        place = self.repository.update_one(place_id, data)
        if place:
            return PlaceSerializer(place).data
        return None

    def update_many(self, filters, data):
        """Update multiple places matching filters."""
        count = self.repository.update_many(filters, data)
        return {"updated_count": count}

    def remove_one(self, place_id):
        """Delete a place by ID."""
        success = self.repository.remove_one(place_id)
        return {"success": success}

    def remove_many(self, filters):
        """Delete multiple places matching filters."""
        count = self.repository.remove_many(filters)
        return {"deleted_count": count}

    def search(self, query):
        """Search places by text."""
        places = self.repository.search(query)
        return PlaceSerializer(places, many=True).data

    def semantic_search(self, query):
        """Semantic search (placeholder for future implementation)."""
        # This would typically use vector embeddings or external search service
        # For now, fall back to regular search
        return self.search(query)

    def filter(self, params):
        """Filter places by parameters."""
        places = self.repository.filter(params)
        return PlaceSerializer(places, many=True).data

    def find_by_id(self, place_id):
        """Find a place by ID."""
        place = self.repository.find_by_id(place_id)
        if place:
            return PlaceSerializer(place).data
        return None

    def find_by_ids(self, place_ids):
        """Find places by multiple IDs."""
        places = self.repository.find_by_ids(place_ids)
        return PlaceSerializer(places, many=True).data

    def exists_by_id(self, place_id):
        """Check if place exists by ID."""
        return {"exists": self.repository.exists_by_id(place_id)}

    def exists_by_ids(self, place_ids):
        """Check which place IDs exist."""
        existing_ids = self.repository.exists_by_ids(place_ids)
        return {"existing_ids": existing_ids}

    # GEO services
    def g_near(self, lat, lng, distance_km=10):
        """Find places near coordinates."""
        places = self.repository.g_near(lat, lng, distance_km)
        return PlaceSerializer(places, many=True).data

    def g_within_box(self, min_lat, min_lng, max_lat, max_lng):
        """Find places within bounding box."""
        places = self.repository.g_within_box(min_lat, min_lng, max_lat, max_lng)
        return PlaceSerializer(places, many=True).data

    def g_within_polygon(self, points):
        """Find places within polygon."""
        places = self.repository.g_within_polygon(points)
        return PlaceSerializer(places, many=True).data

    def g_along_line(self, points, distance_m=100):
        """Find places along a line."""
        places = self.repository.g_along_line(points, distance_m)
        return PlaceSerializer(places, many=True).data

    def g_wkt(self, wkt, operation='intersects'):
        """Find places based on WKT and operation."""
        places = self.repository.g_wkt(wkt, operation)
        return PlaceSerializer(places, many=True).data

    def g_distance(self, lat, lng):
        """Get places with distance from point."""
        places = self.repository.g_distance(lat, lng)
        return PlaceSerializer(places, many=True).data

    def g_buffer(self, lat, lng, radius_m=1000):
        """Find places within buffer around point."""
        places = self.repository.g_buffer(lat, lng, radius_m)
        return PlaceSerializer(places, many=True).data

    def g_intersects(self, geom):
        """Find places that intersect with geometry."""
        places = self.repository.g_intersects(geom)
        return PlaceSerializer(places, many=True).data

    def g_contains(self, geom):
        """Find places that contain geometry."""
        places = self.repository.g_contains(geom)
        return PlaceSerializer(places, many=True).data

    def g_centroid(self):
        """Get centroids of places."""
        places = self.repository.g_centroid()
        return PlaceSerializer(places, many=True).data

    def g_convex_hull(self):
        """Get convex hull of places."""
        places = self.repository.g_convex_hull()
        return PlaceSerializer(places, many=True).data

    def g_cluster(self, grid_size=10):
        """Cluster places."""
        clusters = self.repository.g_cluster(grid_size)
        # Note: This returns raw data, not serialized places
        return clusters

    def g_k_nearest(self, lat, lng, k=5):
        """Find k nearest places to point."""
        places = self.repository.g_k_nearest(lat, lng, k)
        return PlaceSerializer(places, many=True).data

    def g_path_snap(self, points):
        """Snap places to a path."""
        places = self.repository.g_path_snap(points)
        return PlaceSerializer(places, many=True).data