from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .services import follow_user, unfollow_user


User = get_user_model()


@login_required
@require_POST
def follow_view(request, username):
    user_to_follow = get_object_or_404(User, username=username)

    if user_to_follow == request.user:
        messages.error(request, "You cannot follow yourself.")
        return redirect("accounts:profile_detail", username=username)

    follow_user(follower=request.user, following=user_to_follow)
    messages.success(request, f"You are now following @{user_to_follow.username}.")

    return redirect("accounts:profile_detail", username=username)


@login_required
@require_POST
def unfollow_view(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)

    unfollow_user(follower=request.user, following=user_to_unfollow)
    messages.success(request, f"You unfollowed @{user_to_unfollow.username}.")

    return redirect("accounts:profile_detail", username=username)