from django.contrib import admin

from .models import Follow


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("follower", "following", "created_at")
    search_fields = (
        "follower__username",
        "follower__email",
        "following__username",
        "following__email",
    )
    list_filter = ("created_at",)
    ordering = ("-created_at",)