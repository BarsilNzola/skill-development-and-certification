from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    location = models.CharField(max_length=100)
    skills = models.TextField()
    goals = models.TextField()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions'
    )
