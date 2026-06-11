from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


def home_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:profile")

    return redirect("accounts:login")


urlpatterns = [
    path("", home_view, name="home"),
    path("accounts/", include("accounts.urls")),
    path("admin/", admin.site.urls),
]