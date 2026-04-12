from django.contrib import auth
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import User, Profile, Photo, Like, Comments, Follow
from .forms import UserRegisterForm, UserCreateForm
from django.shortcuts import get_object_or_404

def register(request):
    form = UserRegisterForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('profile')
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('profile')
        else:
            return redirect('login')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile(request):
    profile = Profile.objects.get(user=request.user)
    photos = Photo.objects.filter(profile=profile)
    return render(request, 'profile.html', {'profile': profile, 'photos': photos})

def create_post(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserCreateForm(request.POST)

        if form.is_valid():
            photo = form.save(commit=False)
            photo.profile = profile
            photo.save()
            return redirect('profile')
    else:
        form = UserCreateForm()
    return render(request, 'create_post.html', {'form': form})

def detail(request, id):
    profile = Profile.objects.get(user=request.user)
    photo = Photo.objects.get(id=id)
    return render(request, 'detail.html', {'profile': profile, 'photo': photo})

def delete_post(request, id):
    profile = Profile.objects.get(user=request.user)
    photo = Photo.objects.get(id=id)
    photo.delete()
    return redirect('profile')

def like_post(request, id):
    photo = Photo.objects.get(id=id)
    Like.objects.get_or_create(photo=photo, user=request.user)
    return redirect('detail', id=id)

def unlike_post(request, id):
    photo = Photo.objects.get(id=id)
    Like.objects.filter(photo=photo, user=request.user).delete()
    return redirect('detail', id=id)

User = get_user_model()

def search(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username=query).first()
    photos = Photo.objects.filter(Q(profile__user__username__icontains=query))
    return render(request,'search.html', {'users': users, 'photos': photos})

def search_detail(request, id):
    photo = Photo.objects.get(id=id)
    return render(request, 'search_detail.html', {'photo': photo})

def search_like_post(request, id):
    photo = Photo.objects.get(id=id)
    Like.objects.get_or_create(photo=photo, user=request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def search_unlike_post(request, id):
    photo = Photo.objects.get(id=id)
    Like.objects.filter(photo=photo, user=request.user).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def follow_user(request, id):
    user_to_follow = User.objects.get(id=id)
    if request.user != user_to_follow:
        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def unfollow_user(request, id):
    user_to_unfollow = User.objects.get(id=id)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def feed(request):
    following_user = (Follow.objects.filter(follower=request.user)
                      .values_list('following', flat=True))
    following_users = list(following_user)
    following_users.append(request.user.id)
    photos = Photo.objects.filter(profile__user__id__in=following_users).order_by('-created_at')
    return render(request, 'feed.html', {'photos': photos})

def search_comments(request, id):
    photo = Photo.objects.get(id=id)
    if request.method == 'POST':
        Comments.objects.create(user=request.user, photo=photo, comment=request.POST.get('comment'))
        return redirect('search_comments', id=id)
    comments = Comments.objects.filter(photo=photo)
    return render(request, 'search_comments.html', {'photo': photo, 'comments': comments})

def profile_user(request, id):
    user = get_object_or_404(User, id=id)
    profile = Profile.objects.get(user=user)
    photos = Photo.objects.filter(profile=profile)
    return render(request, 'profile_user.html',
                  {'user': user, 'profile': profile, 'photos': photos})