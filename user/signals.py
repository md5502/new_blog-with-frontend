from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import UserProfile
from django.contrib.auth.models import User

def CreateProfile(sender, instance, created,**kwargs):
    if created:
        user = instance
        profile = UserProfile.objects.create(
            user = user,
            email = user.email,
            name = user.username,
        )

def DeleteProfile(sender, instance, **kwargs):
    user = instance.user
    user.delete()

post_save.connect(CreateProfile, sender=User)

post_delete.connect(DeleteProfile, sender=UserProfile)