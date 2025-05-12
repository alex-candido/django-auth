# django_app/modules/v1/users/admin.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom User model for future extensibility.
    
    This model extends Django's AbstractUser, allowing us to add custom fields
    while maintaining all the default User functionality.
    """
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set', 
        blank=True
    )
