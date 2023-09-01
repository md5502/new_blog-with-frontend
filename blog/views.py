from django.shortcuts import redirect, render
from .forms import PostCreateForm, CommentCreateForm, TagCreateForm
from .models import Post, Comment, Tag
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    posts = Post.objects.all()
    return render(request=request, template_name="Post/home.html", context={'posts': posts})


def show_post(request, pk):
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, " Comment has been Added successfully.")
            return redirect(show_post, pk=pk)
    else:
        form = CommentCreateForm()

    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post_id=pk)
    return render(request=request, template_name="Post/post.html", context={'post': post, 'form': form, 'comments': comments})


@login_required(login_url='login')
def create_post(request):
    form = PostCreateForm()
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, " Post has been Created successfully.")
            return redirect(home)

    return render(request, template_name='Post/create_post.html', context={'form': form})


@login_required(login_url='login')
def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    msg = messages.warning(
        request, f"{post.title} has been deleted successfully.")
    return redirect(home)


@login_required(login_url='login')
def update_post(request, pk):
    post = Post.objects.get(id=pk)
    form = PostCreateForm(instance=post)

    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.info(request, " Post has been Created successfully.")
            return redirect(home)

    return render(request, template_name='Post/create_post.html', context={'form': form})


def category(request):
    tags = Tag.objects.all()

    form = TagCreateForm()
    if request.method == 'POST':
        form = TagCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, " Category has been Created successfully.")
            return redirect(category)
    return render(request=request, template_name='Post/category.html', context={'tags': tags, 'form': form})


def Show_category_posts(request, cat):
    posts = Post.objects.filter(tags=cat)
    return render(request=request, template_name="Post/home.html", context={'posts': posts})


def show_cat_posts(request, cat):
    tag = Tag.objects.get(name=cat)
    posts_with_tag = Post.objects.filter(tags=tag)
    return render(request=request, template_name="Post/cat_post.html", context={'posts': posts_with_tag, 'tag_name': cat})
