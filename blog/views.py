from django.shortcuts import redirect, render
from .forms import PostCreateForm, CommentCreateForm
from .models import Post
from django.contrib import messages
# Create your views here.

def home(request):
    posts = Post.objects.all()

    return render(request=request, template_name="Post/home.html", context={'posts': posts}) 


def show_post(request, pk):
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            form.save()
            msg = messages.success(request, " Comment has been Created successfully.")
            return redirect(show_post, pk=pk)
    else:
        form = CommentCreateForm()

    post = Post.objects.get(id = pk)
    return render(request=request, template_name="Post/post.html", context={'post': post, 'comment_form': form}) 

def create_post(request):
    form = PostCreateForm()
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            msg = messages.success(request, " Post has been Created successfully.")
            return redirect(home)

    return render(request, template_name='Post/create_post.html', context={'form' : form})
            

def delet_post(request, pk):
    post = Post.objects.get(id = pk)
    post.delete()
    msg = messages.success(request, f"{post.title} has been deleted successfully.")
    return redirect(home)

def update_post(request, pk):
    post = Post.objects.get(id=pk)
    form = PostCreateForm(instance=post)

    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            msg = messages.success(request, " Post has been Created successfully.")
            return redirect(home)

    return render(request, template_name='Post/create_post.html', context={'form' : form})
      

