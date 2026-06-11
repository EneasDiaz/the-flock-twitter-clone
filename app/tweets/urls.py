from django.urls import path

from .views import create_tweet_view, delete_tweet_view, timeline_view

app_name = "tweets"

urlpatterns = [
    path("", timeline_view, name="timeline"),
    path("create/", create_tweet_view, name="create"),
    path("<int:tweet_id>/delete/", delete_tweet_view, name="delete"),
]