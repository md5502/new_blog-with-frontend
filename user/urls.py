from django.urls import path
from .views import userprofile
urlpatterns = [
    path('profile/', view=userprofile, name='userprofile')
]