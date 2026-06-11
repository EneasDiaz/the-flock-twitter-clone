from django.urls import path

from .views import follow_view, unfollow_view

app_name = "follows"

urlpatterns = [
    path("<str:username>/follow/", follow_view, name="follow"),
    path("<str:username>/unfollow/", unfollow_view, name="unfollow"),
]