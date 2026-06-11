from django.urls import path

from .views import like_tweet_view, unlike_tweet_view

app_name = "likes"

urlpatterns = [
    path("tweets/<int:tweet_id>/like/", like_tweet_view, name="like"),
    path("tweets/<int:tweet_id>/unlike/", unlike_tweet_view, name="unlike"),
]