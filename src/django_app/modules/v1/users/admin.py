# django_app/modules/v1/users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django_app.modules.v1.users.models import User

# Customize the User admin interface
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'last_login')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)

