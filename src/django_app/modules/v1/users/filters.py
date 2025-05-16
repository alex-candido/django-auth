# django_app/modules/v1/users/filters.py

import django_filters
from .models import User

class UserFilter(django_filters.FilterSet):
    uuid = django_filters.UUIDFilter()
    username = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains') 
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    date_joined = django_filters.DateFromToRangeFilter()
    last_login = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = User
        fields = ['uuid', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login']