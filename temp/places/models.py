# django_app/modules/v1/places/models.py

from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django_app.modules.v1.users.models import User

class Place(models.Model):
    """Model for storing places with geographic information.
    
    This model uses GeoDjango's PointField to store geographic coordinates
    and provides spatial functionality for location-based queries.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    location = gis_models.PointField(geography=True, default=Point(0.0, 0.0))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='places')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Place'
        verbose_name_plural = 'Places'
    
    def __str__(self):
        return self.name
    
    @property
    def latitude(self):
        return self.location.y
    
    @property
    def longitude(self):
        return self.location.x