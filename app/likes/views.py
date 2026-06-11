from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from tweets.models import Tweet

from .services import like_tweet, unlike_tweet


@login_required
@require_POST
def like_tweet_view(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)

    like_tweet(user=request.user, tweet=tweet)
    messages.success(request, "Tweet liked.")

    return redirect("tweets:timeline")


@login_required
@require_POST
def unlike_tweet_view(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)

    unlike_tweet(user=request.user, tweet=tweet)
    messages.success(request, "Tweet unliked.")

    return redirect("tweets:timeline")