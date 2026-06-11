from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import TweetForm
from .models import Tweet


@login_required
def timeline_view(request):
    tweets = Tweet.objects.filter(author=request.user).select_related("author")

    paginator = Paginator(tweets, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "tweets/timeline.html",
        {
            "form": TweetForm(),
            "page_obj": page_obj,
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
        messages.error(request, "Tweet must be between 1 and 280 characters.")

    return redirect("tweets:timeline")


@login_required
@require_POST
def delete_tweet_view(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id, author=request.user)
    tweet.delete()

    messages.success(request, "Tweet deleted.")
    return redirect("tweets:timeline")