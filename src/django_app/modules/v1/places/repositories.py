# django_app/modules/v1/places/repositories.py

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point, Polygon
from django.contrib.gis.measure import D
from django.db.models import Q, F
from django.utils.text import slugify
import uuid
from typing import List, Dict, Any, Optional

from .models import Place

class PlaceRepository:
    def find_one(self, params):
        """Find a single place based on filter parameters."""
        try:
            filters = {}
            if params.id is not None:
                filters['id'] = params.id
            if params.uuid is not None:
                filters['uuid'] = params.uuid
            if params.slug is not None:
                filters['slug'] = params.slug
            if params.name is not None:
                filters['name'] = params.name
                
            return Place.objects.filter(**filters).first()
        except Exception as e:
            print(f"Error in find_one: {str(e)}")
            return None

    def find_all(self, page=1, per_page=10, sort='id', sort_dir='asc', filters=None):
        """Find all places with pagination and sorting."""
        try:
            queryset = Place.objects.all()
            
            # Apply filters if provided
            if filters:
                filter_dict = {}
                for key, value in filters.items():
                    if value is not None:
                        filter_dict[key] = value
                if filter_dict:
                    queryset = queryset.filter(**filter_dict)
            
            # Apply sorting
            sort_field = sort
            if sort_dir.lower() == 'desc':
                sort_field = f'-{sort_field}'
            queryset = queryset.order_by(sort_field)
            
            # Apply pagination
            total = queryset.count()
            offset = (page - 1) * per_page
            items = queryset[offset:offset + per_page]
            
            last_page = (total + per_page - 1) // per_page  # Ceiling division
            
            return {
                'items': items,
                'total': total,
                'current_page': page,
                'per_page': per_page,
                'last_page': last_page
            }
        except Exception as e:
            print(f"Error in find_all: {str(e)}")
            return {
                'items': [],
                'total': 0,
                'current_page': page,
                'per_page': per_page,
                'last_page': 0
            }

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
            place = Place.objects.get(id=place_id)
            
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

    def update_many(self, places_data):
        """Update multiple places."""
        updated_places = []
        for place_data in places_data:
            place_id = place_data.pop('id', None)
            if place_id:
                place = self.update_one(place_id, place_data)
                if place:
                    updated_places.append(place)
        return updated_places

    def remove_one(self, place_id):
        """Remove a place by ID."""
        try:
            place = Place.objects.get(id=place_id)
            place.delete()
            return True
        except Place.DoesNotExist:
            return False
        except Exception as e:
            print(f"Error in remove_one: {str(e)}")
            return False

    def remove_many(self, place_ids):
        """Remove multiple places by IDs."""
        try:
            Place.objects.filter(id__in=place_ids).delete()
            return True
        except Exception as e:
            print(f"Error in remove_many: {str(e)}")
            return False

    def search(self, query, field, page=1, per_page=10, sort='id', sort_dir='asc'):
        """Search places by a specific field."""
        try:
            filter_kwargs = {f"{field}__icontains": query}
            queryset = Place.objects.filter(**filter_kwargs)
            
            # Apply sorting
            sort_field = sort
            if sort_dir.lower() == 'desc':
                sort_field = f'-{sort_field}'
            queryset = queryset.order_by(sort_field)
            
            # Apply pagination
            total = queryset.count()
            offset = (page - 1) * per_page
            items = queryset[offset:offset + per_page]
            
            last_page = (total + per_page - 1) // per_page  # Ceiling division
            
            return {
                'items': items,
                'total': total,
                'current_page': page,
                'per_page': per_page,
                'last_page': last_page
            }
        except Exception as e:
            print(f"Error in search: {str(e)}")
            return {
                'items': [],
                'total': 0,
                'current_page': page,
                'per_page': per_page,
                'last_page': 0
            }

    def filter(self, filters, page=1, per_page=10, sort='id', sort_dir='asc'):
        """Filter places by multiple criteria."""
        try:
            queryset = Place.objects.all()
            
            # Apply filters
            if filters:
                filter_dict = {}
                for key, value in filters.items():
                    if value is not None:
                        filter_dict[key] = value
                if filter_dict:
                    queryset = queryset.filter(**filter_dict)
            
            # Apply sorting
            sort_field = sort
            if sort_dir.lower() == 'desc':
                sort_field = f'-{sort_field}'
            queryset = queryset.order_by(sort_field)
            
            # Apply pagination
            total = queryset.count()
            offset = (page - 1) * per_page
            items = queryset[offset:offset + per_page]
            
            last_page = (total + per_page - 1) // per_page  # Ceiling division
            
            return {
                'items': items,
                'total': total,
                'current_page': page,
                'per_page': per_page,
                'last_page': last_page
            }
        except Exception as e:
            print(f"Error in filter: {str(e)}")
            return {
                'items': [],
                'total': 0,
                'current_page': page,
                'per_page': per_page,
                'last_page': 0
            }

    def find_by_id(self, place_id):
        """Find a place by ID."""
        try:
            return Place.objects.get(id=place_id)
        except Place.DoesNotExist:
            return None
        except Exception as e:
            print(f"Error in find_by_id: {str(e)}")
            return None

    def find_by_ids(self, place_ids):
        """Find multiple places by IDs."""
        try:
            return list(Place.objects.filter(id__in=place_ids))
        except Exception as e:
            print(f"Error in find_by_ids: {str(e)}")
            return []

    def exists_by_id(self, place_id):
        """Check if a place exists by ID."""
        return Place.objects.filter(id=place_id).exists()

    def exists_by_ids(self, place_ids):
        """Check if multiple places exist by IDs."""
        existing_ids = Place.objects.filter(id__in=place_ids).values_list('id', flat=True)
        results = []
        for place_id in place_ids:
            results.append({
                'id': place_id,
                'exists': place_id in existing_ids
            })
        return results

    # Geo-specific methods
    
    def g_near(self, latitude, longitude, radius=5000, page=1, per_page=10, sort='id', sort_dir='asc'):
        """Find places near a point within a radius (in meters)."""
        try:
            point = Point(longitude, latitude, srid=4326)
            queryset = Place.objects.filter(location__distance_lte=(point, D(m=radius)))
            
            # Add distance annotation
            queryset = queryset.annotate(distance=Distance('location', point))
            
            # Apply sorting (default to distance if not specified)
            sort_field = 'distance' if sort == 'id' else sort
            if sort_dir.lower() == 'desc' and sort_field == 'distance':
                sort_field = '-distance'
            elif sort_dir.lower() == 'desc':
                sort_field = f'-{sort_field}'
            queryset = queryset.order_by(sort_field)
            
            # Apply pagination
            total = queryset.count()
            offset = (page - 1) * per_page
            items = queryset[offset:offset + per_page]
            
            last_page = (total + per_page - 1) // per_page  # Ceiling division
            
            return {
                'items': items,
                'total': total,
                'current_page': page,
                'per_page': per_page,
                'last_page': last_page
            }
        except Exception as e:
            print(f"Error in g_near: {str(e)}")
            return {
                'items': [],
                'total': 0,
                'current_page': page,
                'per_page': per_page,
                'last_page': 0
            }

    def g_within_box(self, min_lat, min_lng, max_lat, max_lng, page=1, per_page=10, sort='id', sort_dir='asc'):
        """Find places within a bounding box."""
        try:
            # Create polygon from bounding box coordinates
            bbox = Polygon.from_bbox((min_lng, min_lat, max_lng, max_lat))
            queryset = Place.objects.filter(location__contained=bbox)
            
            # Apply sorting
            sort_field = sort
            if sort_dir.lower() == 'desc':
                sort_field = f'-{sort_field}'
            queryset = queryset.order_by(sort_field)
            
            # Apply pagination
            total = queryset.count()
            offset = (page - 1) * per_page
            items = queryset[offset:offset + per_page]
            
            last_page = (total + per_page - 1) // per_page  # Ceiling division
            
            return {
                'items': items,
                'total': total,
                'current_page': page,
                'per_page': per_page,
                'last_page': last_page
            }
        except Exception as e:
            print(f"Error in g_within_box: {str(e)}")
            return {
                'items': [],
                'total': 0,
                'current_page': page,
                'per_page': per_page,
                'last_page': 0
            }