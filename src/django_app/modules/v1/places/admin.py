# django_app/modules/v1/places/admin.py

from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Place

@admin.register(Place)
class PlaceAdmin(OSMGeoAdmin):
    list_display = ('name', 'type', 'status', 'city', 'country', 'created_at')
    list_filter = ('type', 'status', 'city', 'country')
    search_fields = ('name', 'city', 'state', 'country')
    ordering = ('-created_at',)
    