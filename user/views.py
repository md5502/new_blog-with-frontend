from django.shortcuts import render ,redirect
from .models import UserProfile
from blog.models import Post
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .form import CustomUserCreationForm, EditUserProfile
from django.contrib import messages
# Create your views here.

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        messages.info(request, "You are Already logged in")
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username = username)
        except:
            print('user name dose not exist')
        
        user = authenticate(request=request, username=username, password = password)

        if user is not None:
            login(request=request, user=user)
            messages.success(request, "you'r logged in ")
            return redirect('home')
        else:
            messages.warning(request, "username or password is incorrect")
            
    return render(request, template_name='user/login_register.html',  context={'page': page})


def logoutUser(request):
    logout(request=request)
    messages.success(request, "you'r logged OUT ")

    return redirect(loginUser)

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
       form = CustomUserCreationForm(request.POST)
       if form.is_valid():
           user = form.save(commit=False)
           user.username = user.username.lower()
           user.save()

           messages.success(request, 'the User accost was created')
           login(request, user)
           return redirect('home')
       else:
           messages.warning(request, 'an error has occurred during registration')
    return render(request, template_name='user/login_register.html', context={'page': page, 'form': form})


def userprofile(request, pk):
    user = User.objects.get(id=pk)
    userprofile = UserProfile.objects.get(user = user)

    posts = Post.objects.filter(owner_id=userprofile.id)
    
    post_count = len(posts)
    return render(request, template_name='user/userProfile.html', context={'profile': userprofile, 'post_count': post_count, 'posts': posts})



def EditProfile(request, pk):
    profile = UserProfile.objects.get(id = pk)
    form = EditUserProfile(instance=profile)
    if request.method == 'POST':
        form = EditUserProfile(request.POST, request.FILES, instance=profile)
        if form.is_valid:
            form.save()
            messages.info(request, "Profile has been Created successfully.")
            return redirect(userprofile, pk=profile.user.id)
    
    return render(request, template_name='user/EditUserProfile.html', context={'form': form})

def DeleteProfile(request, pk):
    profile = UserProfile.objects.get(id = pk)
    profile.delete()
    messages.warning(request, 'Profile has been deleted successfully')
    return redirect('home')