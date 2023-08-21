from django.urls import path
from .views import home, show_post, create_post, delet_post, update_post

urlpatterns=[
    path('', home, name='home'),
    path('single_post/<str:pk>', name='single_post', view=show_post),
    path('create_post/', name='create_post', view=create_post),
    path('delet_post/<str:pk>', name='delet_post', view=delet_post),
    path('update_post/<str:pk>', name='update_post', view=update_post),
]