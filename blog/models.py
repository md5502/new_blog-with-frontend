from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Post(models.Model):
    POBLISH_CH = (
        ('P', 'Poblished'),
        ('D', 'Draft')
    )
    title = models.CharField(max_length=200)
    body = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=POBLISH_CH)
    tags = models.ManyToManyField('Tag', null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(unique=True, primary_key=True, default=uuid.uuid4, editable=False, max_length=200)

    def __str__(self):
        return self.title
    

class Tag(models.Model):
    name=models.CharField(max_length=120)

    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(unique=True, primary_key=True, default=uuid.uuid4, editable=False, max_length=200)

    def __str__(self):
        return self.name


    