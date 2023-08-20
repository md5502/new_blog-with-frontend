from django.shortcuts import redirect, render
from .forms import PostCreateForm
from .models import Post
# Create your views here.

def home(request):
    posts = Post.objects.all()

    return render(request=request, template_name="Post/home.html", context={'posts': posts}) 


def show_post(request, pk):
    post = Post.objects.get(id = pk)
    print(post, '\n\n\n')
    return render(request=request, template_name="Post/single_post.html", context={'post': post}) 

def create_post(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        form.save()
        return redirect(home)
    else:
        form = PostCreateForm()
    return render(request, template_name='Post/create_post.html', context={'form' : form})
            