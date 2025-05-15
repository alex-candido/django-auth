# django_app/modules/v1/places/utils.py

from django.contrib.gis.geos import Point, Polygon, LineString, MultiPolygon, GEOSGeometry
from django.contrib.gis.measure import D


class GeoUtils:
    """Utility class for geospatial operations."""
    
    @staticmethod
    def point_from_lat_lng(lat, lng):
        """Create a point from latitude and longitude."""
        return Point(float(lng), float(lat), srid=4326)
    
    @staticmethod
    def bbox_to_polygon(min_lat, min_lng, max_lat, max_lng):
        """Convert bounding box to polygon."""
        return Polygon.from_bbox((float(min_lng), float(min_lat), float(max_lng), float(max_lat)))
    
    @staticmethod
    def points_to_linestring(points):
        """Convert list of [lng, lat] points to LineString."""
        if not points or len(points) < 2:
            raise ValueError("LineString requires at least 2 points")
        return LineString(points, srid=4326)
    
    @staticmethod
    def points_to_polygon(points):
        """Convert list of [lng, lat] points to Polygon."""
        if not points or len(points) < 3:
            raise ValueError("Polygon requires at least 3 points")
        
        # Ensure polygon is closed
        if points[0] != points[-1]:
            points.append(points[0])
        
        return Polygon(points, srid=4326)
    
    @staticmethod
    def wkt_to_geometry(wkt_string):
        """Convert WKT string to GEOSGeometry."""
        try:
            return GEOSGeometry(wkt_string, srid=4326)
        except Exception as e:
            raise ValueError(f"Invalid WKT string: {str(e)}")
    
    @staticmethod
    def buffer_point(point, distance_m):
        """Create a buffer around a point in meters."""
        # For more accurate measurements on a geographical coordinate system
        return point.buffer(distance_m / 100000.0)  # Approximate in degrees
    
    @staticmethod
    def distance_between_points(point1, point2):
        """Calculate distance between two points in meters."""
        return point1.distance(point2) * 100000.0  # Approximate conversion to meters
    
    @staticmethod
    def haversine_distance(lat1, lng1, lat2, lng2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        from math import radians, cos, sin, asin, sqrt
        
        # Convert decimal degrees to radians
        lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])

        # Haversine formula
        dlon = lng2 - lng1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers
        return c * r * 1000  # Convert to meters
    
    @staticmethod
    def simplify_geometry(geom, tolerance=0.001):
        """Simplify a geometry with given tolerance."""
        return geom.simplify(tolerance, preserve_topology=True)
    
    @staticmethod
    def geo_hash(lat, lng, precision=7):
        """Generate geohash for given coordinates."""
        try:
            import geohash
            return geohash.encode(float(lat), float(lng), precision=precision)
        except ImportError:
            # Simple fallback if geohash module is not available
            lat_encoded = round(float(lat), precision)
            lng_encoded = round(float(lng), precision)
            return f"{lat_encoded}:{lng_encoded}"
    
    @staticmethod
    def geojson_to_geometry(geojson_dict):
        """Convert GeoJSON dict to GEOSGeometry."""
        import json
        geojson_str = json.dumps(geojson_dict)
        return GEOSGeometry(geojson_str)
    
    @staticmethod
    def geometry_to_geojson(geom):
        """Convert GEOSGeometry to GeoJSON dict."""
        return {
            "type": geom.geom_type,
            "coordinates": geom.coords
        }