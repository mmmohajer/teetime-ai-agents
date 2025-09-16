from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import UserModel, ProfileModel

@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ProfileModel.objects.create(user=instance)
