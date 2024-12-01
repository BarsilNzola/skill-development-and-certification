from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

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
    profile = models.OneToOneField(
        'core.UserProfile',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='custom_user_profile'
    )

class UserProgress(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    progress_percentage = models.IntegerField(default=0)