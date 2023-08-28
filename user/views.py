from django.shortcuts import render
from .models import UserProfile
from blog.models import Post
# Create your views here.

def userprofile(request):
    userprofile = UserProfile.objects.first()
    posts = Post.objects.filter(owner_id=userprofile.id)
    post_count = len(posts)
    return render(request, template_name='user/userProfile.html', context={'profile': userprofile, 'post_count': post_count, 'posts': posts})
