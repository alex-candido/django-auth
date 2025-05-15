# django_app/modules/v1/places/admin.py

from django.contrib import admin
from .models import Place

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'status', 'city', 'country', 'created_at')
    list_filter = ('type', 'status', 'city', 'country')
    search_fields = ('name', 'city', 'state', 'country')
    ordering = ('-created_at',)
    