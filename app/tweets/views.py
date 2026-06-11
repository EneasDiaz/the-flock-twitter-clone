from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db.models import Count, Q
from follows.models import Follow

from .forms import TweetForm
from .models import Tweet


@login_required
def timeline_view(request):
    following_ids = Follow.objects.filter(follower=request.user,).values_list("following_id", flat=True)
    tweets = (Tweet.objects.filter(Q(author=request.user) | Q(author_id__in=following_ids)).select_related("author").annotate(likes_count=Count("likes")).order_by("-created_at"))

    liked_tweet_ids = set(request.user.likes.values_list("tweet_id", flat=True))

    paginator = Paginator(tweets, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "tweets/timeline.html",
        {
            "form": TweetForm(),
            "page_obj": page_obj,
            "liked_tweet_ids": liked_tweet_ids,
        },
    )


@login_required
@require_POST
def create_tweet_view(request):
    form = TweetForm(request.POST)

    if form.is_valid():
        tweet = form.save(commit=False)
        tweet.author = request.user
        tweet.save()
        messages.success(request, "Tweet created.")
    else:
        messages.error(request, "Tweet must have text and be no longer than 280 characters.")

    return redirect("tweets:timeline")


@login_required
@require_POST
def delete_tweet_view(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id, author=request.user)
    tweet.delete()

    messages.success(request, "Tweet deleted.")
    return redirect("tweets:timeline")