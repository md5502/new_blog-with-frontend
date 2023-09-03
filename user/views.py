from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from blog.models import Post, Comment
from .forms import CustomUserCreationForm, EditUserProfile

def loginUser(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.warning(request, "Username does not exist.")
            return redirect('login')
        
        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            login(request=request, user=user)
            messages.success(request, "You're logged in.")
            return redirect('home')
        else:
            messages.warning(request, "Username or password is incorrect.")
    
    return render(request, template_name='user/login_register.html', context={'page': 'login'})

def logoutUser(request):
    logout(request=request)
    messages.success(request, "You're logged out.")
    return redirect('login')

def registerUser(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already registered and logged in.")
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            
            login(request, user)
            messages.success(request, 'The user account was created.')
            return redirect('home')
        else:
            messages.warning(request, 'An error occurred during registration.')
    else:
        form = CustomUserCreationForm()

    return render(request, template_name='user/login_register.html', context={'page': 'register', 'form': form})

@login_required(login_url='login')
def userprofile(request, pk):
    user = get_object_or_404(User, id=pk)
    userprofile = get_object_or_404(UserProfile, user=user)
    posts = Post.objects.filter(owner_id=userprofile.id)
    posts_comments = []
    for post in posts:
        comments_count = len(Comment.objects.filter(post = post))
        post.comments = comments_count
    post_count = len(posts)
    return render(request, template_name='user/userProfile.html', context={'profile': userprofile, 'post_count': post_count, 'posts': posts})

@login_required(login_url='login')
def EditProfile(request, pk):
    profile = get_object_or_404(UserProfile, id=pk)
    form = EditUserProfile(instance=profile)


    if request.user != profile.user:
        messages.error(request, "You don't have permission to edit this profile.")
        return redirect('home')
    
    if request.method == 'POST':
        form = EditUserProfile(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Profile has been updated successfully.")
            return redirect('userprofile', pk=profile.user.id)
    
    return render(request, template_name='user/EditUserProfile.html', context={'form': form})

@login_required(login_url='login')
def DeleteProfile(request, pk):
    profile = UserProfile.objects.get(id=pk)
    if request.user != profile.user:
        messages.error(request, "You don't have permission to edit this profile.")
        return redirect('home')
    else:
        profile.delete()
    
    messages.warning(request, 'Profile has been deleted successfully.')
    return redirect('home')
