
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('tweet', views.tweet, name='tweet'),
    path('<int:profile_id>', views.profile, name='profile'),
    path('follow/<int:account_id>', views.follow_user, name="follow_user"),
    path('like/<str:post_type>/<int:post_id>', views.like_post, name="like_post")
]
