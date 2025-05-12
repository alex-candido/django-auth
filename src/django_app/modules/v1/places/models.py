# django_app/modules/v1/places/models.py

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

class Place(models.Model):
    """Model for storing geographic places with spatial data."""

    class PlaceStatus(models.IntegerChoices):
        ACTIVE = 0, 'Active'
        INACTIVE = 1, 'Inactive'

    class PlaceType(models.IntegerChoices):
        BAR = 0, 'Bar'
        PUB = 1, 'Pub'
        RESTAURANT = 2, 'Restaurant'
        CAFE = 3, 'Cafe'
        NIGHTCLUB = 4, 'Nightclub'
        BREWERY = 5, 'Brewery'
        WINERY = 6, 'Winery'
        FOOD_TRUCK = 7, 'Food Truck'
        COCKTAIL_BAR = 8, 'Cocktail Bar'
        SPORTS_BAR = 9, 'Sports Bar'
        LOUNGE = 10, 'Lounge'
        ROOFTOP_BAR = 11, 'Rooftop Bar'

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    location = models.PointField(geography=True, srid=4326)

    website = models.URLField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    type = models.IntegerField(choices=PlaceType.choices, default=PlaceType.BAR)
    status = models.IntegerField(choices=PlaceStatus.choices, default=PlaceStatus.ACTIVE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.get_type_display()})'
    
    def latitude(self):
        return self.location.y if self.location else None
    
    def longitude(self):
        return self.location.x if self.location else None
    
    def set_location(self, lat, lng):
        self.location = Point(lng, lat, srid=4326)

    class Meta:
        db_table = 'places'
