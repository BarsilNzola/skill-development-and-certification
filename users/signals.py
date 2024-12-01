from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from core.models import UserProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print(f"Creating UserProfile for user: {instance.username}")
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    print(f"Saving UserProfile for user: {instance.username}")
    instance.profile.save()
