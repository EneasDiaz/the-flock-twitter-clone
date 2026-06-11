from django.contrib import admin

from .models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "tweet", "created_at")
    search_fields = ("user__username", "user__email", "tweet__content")
    list_filter = ("created_at",)
    ordering = ("-created_at",)