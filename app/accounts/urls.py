from django.urls import path

from .views import (
    CustomLoginView,
    CustomLogoutView,
    followers_list_view,
    following_list_view,
    profile_detail_view,
    profile_view,
    register_view,
)

app_name = "accounts"

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("profile/", profile_view, name="profile"),
    path("users/<str:username>/", profile_detail_view, name="profile_detail"),
    path("users/<str:username>/followers/", followers_list_view, name="followers_list"),
    path("users/<str:username>/following/", following_list_view, name="following_list"),
]