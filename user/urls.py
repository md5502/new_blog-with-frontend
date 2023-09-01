from django.urls import path
from .views import userprofile, loginUser, logoutUser, registerUser, EditProfile, DeleteProfile
urlpatterns = [
    path('profile/<str:pk>', view=userprofile, name='userprofile'),
    path('login/', view=loginUser, name='login'),
    path('register/', view=registerUser, name='register'),
    path('logout/', view=logoutUser, name='logout'),
    path('edit-profile/<str:pk>', view=EditProfile, name='EditProfile'),
    path('delete-profile/<str:pk>', view=DeleteProfile, name='delete-profile'),
]