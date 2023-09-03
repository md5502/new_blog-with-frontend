from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.db import models
from .forms import CommentCreateForm, TagCreateForm, PostCreateForm
from .models import Post, Comment, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required



def home(request):
    posts_per_page = 10  # Adjust this value as desired

    all_posts = Post.objects.filter(status = 'P')

    paginator = Paginator(all_posts, posts_per_page)

    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(
        request=request,
        template_name="Post/home.html",
        context={'posts': posts}
    )

def show_post(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, "Comment has been added successfully.")
            return redirect('show_post', pk=pk)
    else:
        form = CommentCreateForm()

    comments = Comment.objects.filter(post=post)
    return render(request=request, template_name="Post/post.html", context={'post': post, 'form': form, 'comments': comments})

@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user.userprofile
            post.save()

            # Handle tags separately
            tag_names = request.POST.get('tags', '').split(',')
            for tag_name in tag_names:
                tag_name = tag_name.strip()
                if tag_name:
                    # Check if the tag already exists
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag.name)
                    remove_unused_tags()

            messages.success(request, "Post has been created successfully.")
            return redirect('home')
        else:
            messages.error(request, "There was an error in the form submission. Please check the form data.")
    else:
        form = PostCreateForm()

    return render(request, 'Post/create_post.html', {'form': form})

@login_required(login_url='login')
def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user == post.owner.user or request.user.is_staff or request.user.is_superuser:
        post.delete()
        messages.warning(request, f"{post.title} has been deleted successfully.")
    else:
        messages.error(request, "You don't have permission to delete this post.")
    return redirect('home')

@login_required(login_url='login')
def update_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    
    if post.owner.user != request.user:
        messages.error(request, "You don't have permission to edit this post.")
        return redirect('home')

    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.info(request, "Post has been updated successfully.")
            return redirect('home')
    else:
        form = PostCreateForm(instance=post)

    return render(request, template_name='Post/create_post.html', context={'form': form})

def category(request):
    tags = Tag.objects.all()
    form = TagCreateForm()
    if request.method == 'POST':
        form = TagCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category has been created successfully.")
            return redirect('category')
    
    return render(request=request, template_name='Post/category.html', context={'tags': tags, 'form': form})

def Show_category_posts(request, cat):
    posts = Post.objects.filter(tags__name=cat)
    return render(request=request, template_name="Post/home.html", context={'posts': posts})

def show_cat_posts(request, cat):
    tag = get_object_or_404(Tag, name=cat)
    posts_with_tag = Post.objects.filter(tags=tag)
    return render(request=request, template_name="Post/cat_post.html", context={'posts': posts_with_tag, 'tag_name': cat})

def remove_unused_tags():
    unused_tags = Tag.objects.annotate(post_count=models.Count('post')).filter(post_count=0)
    unused_tags.delete()