from django.urls import path
from .views import *

urlpatterns = [
    path('', register, name='register'),
    path('login/', login_view, name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('create/', create_post, name='create'),
    path('detail/<int:id>/', detail, name='detail'),
    path('delete/<int:id>/', delete_post, name='delete'),
    path('like/<int:id>/', like_post, name='like'),
    path('unlike/<int:id>/', unlike_post, name='unlike'),
    path('search/', search, name='search'),
    path('search/<int:id>/', search_detail, name='search_detail'),
    path('search/like/<int:id>/', search_like_post, name='search_like'),
    path('search/unlike/<int:id>/', search_unlike_post, name='search_unlike'),
    path('search/follow/<int:id>/', follow_user, name='follow_user'),
    path('search/unfollow/<int:id>/', unfollow_user, name='unfollow_user'),
    path('search/comments/<int:id>/', search_comments, name='search_comments'),
    path('feed/', feed, name='feed'),
    path('profile_user/<int:id>/', profile_user, name='profile_user'),
]