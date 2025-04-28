# django_app/modules/v1/auth/admin.py

from django.contrib import admin
from .models import TokenBlacklist

# Customize the User admin interface
@admin.register(TokenBlacklist)
class TokenBlacklistAdmin(admin.ModelAdmin):
    list_display = ('token', 'blacklisted_at', 'expires_at')
    search_fields = ('token',)
    list_filter = ('blacklisted_at', 'expires_at')
