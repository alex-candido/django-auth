# django_app/modules/v1/places/filters.py

from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Place


class PlaceFilter(filters.FilterSet):
    """Filter for Place model."""
    name = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    address = filters.CharFilter(lookup_expr='icontains')
    city = filters.CharFilter(lookup_expr='icontains')
    state = filters.CharFilter(lookup_expr='icontains')
    country = filters.CharFilter(lookup_expr='icontains')
    postal_code = filters.CharFilter(lookup_expr='icontains')

    type = filters.MultipleChoiceFilter(choices=Place.PlaceType.choices)
    status = filters.MultipleChoiceFilter(choices=Place.PlaceStatus.choices)

    created_at_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    updated_at_after = filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte')
    updated_at_before = filters.DateTimeFilter(field_name='updated_at', lookup_expr='lte')

    has_website = filters.BooleanFilter(method='filter_has_website')
    has_phone = filters.BooleanFilter(method='filter_has_phone')
    has_email = filters.BooleanFilter(method='filter_has_email')
    has_location = filters.BooleanFilter(method='filter_has_location')

    q = filters.CharFilter(method='filter_search')

    class Meta:
        model = Place
        fields = [
            'name', 'description', 'address', 'city', 'state', 'country',
            'postal_code', 'type', 'status'
        ]

    def filter_has_website(self, queryset, name, value):
        """Filter by presence/absence of website."""
        if value:
            return queryset.exclude(website__isnull=True).exclude(website='')
        return queryset.filter(Q(website__isnull=True) | Q(website=''))

    def filter_has_phone(self, queryset, name, value):
        """Filter by presence/absence of phone."""
        if value:
            return queryset.exclude(phone__isnull=True).exclude(phone='')
        return queryset.filter(Q(phone__isnull=True) | Q(phone=''))

    def filter_has_email(self, queryset, name, value):
        """Filter by presence/absence of email."""
        if value:
            return queryset.exclude(email__isnull=True).exclude(email='')
        return queryset.filter(Q(email__isnull=True) | Q(email=''))

    def filter_has_location(self, queryset, name, value):
        """Filter by presence/absence of geo location."""
        if value:
            return queryset.exclude(location__isnull=True)
        return queryset.filter(location__isnull=True)

    def filter_search(self, queryset, name, value):
        """Generic search across multiple fields."""
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value) |
            Q(address__icontains=value) |
            Q(city__icontains=value) |
            Q(state__icontains=value) |
            Q(country__icontains=value)
        )
