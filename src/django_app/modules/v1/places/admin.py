# django_app/modules/v1/places/admin.py

from django.contrib import admin
from .models import Place

@admin.register(Place)
class PocoAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'type', 'status', 'city', 'country', 'created_at')
    list_filter = ('type', 'status', 'city', 'country')
    search_fields = ('name', 'city', 'state', 'country')
    ordering = ('-created_at',)
    