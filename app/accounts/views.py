from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from follows.services import is_following
from follows.models import Follow

from .forms import EmailAuthenticationForm, RegistrationForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:profile")

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("accounts:profile")
    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    pass


@login_required
def profile_view(request):
    return render(request, "accounts/profile.html")

User = get_user_model()


@login_required
def profile_detail_view(request, username):
    profile_user = get_object_or_404(User, username=username)

    return render(
        request,
        "accounts/profile_detail.html",
        {
            "profile_user": profile_user,
            "is_following_profile": is_following(
                follower=request.user,
                following=profile_user,
            ),
            "followers_count": Follow.objects.filter(following=profile_user).count(),
            "following_count": Follow.objects.filter(follower=profile_user).count(),
        },
    )


@login_required
def followers_list_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    followers = User.objects.filter(
        following_relationships__following=profile_user,
    ).order_by("username")

    return render(
        request,
        "accounts/followers_list.html",
        {
            "profile_user": profile_user,
            "users": followers,
            "list_title": "Followers",
        },
    )


@login_required
def following_list_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    following = User.objects.filter(
        follower_relationships__follower=profile_user,
    ).order_by("username")

    return render(
        request,
        "accounts/following_list.html",
        {
            "profile_user": profile_user,
            "users": following,
            "list_title": "Following",
        },
    )