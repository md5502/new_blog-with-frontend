from django.urls import path
from .views import home, show_post, create_post, delete_post, update_post, category, show_cat_posts

urlpatterns=[
    path('', home, name='home'),
    path('single_post/<str:pk>', name='single_post', view=show_post),
    path('create_post/', name='create_post', view=create_post),
    path('delete_post/<str:pk>', name='delete_post', view=delete_post),
    path('update_post/<str:pk>', name='update_post', view=update_post),
    path('categorys', name='categorys', view=category),
    path('show_cat_posts/<str:cat>', name='show_cat_posts', view=show_cat_posts),
]