from django.urls import path
from .views import home, show_post, create_post

urlpatterns=[
    path('', home, name='home'),
    path('single_post/<str:pk>', name='single_post', view=show_post),
    path('create_post/', name='create_post', view=create_post),
]