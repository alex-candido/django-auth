# django_app/modules/v1/auth/models.py

from django.db import models
from django.utils import timezone

class TokenBlacklist(models.Model):
    token = models.CharField(max_length=500)
    blacklisted_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = 'token_blacklist'
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['expires_at'])
        ]

    def __str__(self):
        return f"{self.token[:50]}... (Blacklisted at {self.blacklisted_at})"

# Create your models here.
