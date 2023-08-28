from django.db import models
from django.contrib.auth.models import User
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True )
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, default='profile_pics/def_profile.png')
    bio = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    # Additional fields
    twitter_username = models.CharField(max_length=50, blank=True, null=True)
    instagram_username = models.CharField(max_length=50, blank=True, null=True)
    facebook_profile = models.URLField(blank=True, null=True)
    linkedin_profile = models.URLField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(unique=True, primary_key=True, default=uuid.uuid4, editable=False, max_length=200)


    def __str__(self):
        return self.user.username
