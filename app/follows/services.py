from django.core.exceptions import ValidationError

from .models import Follow


def follow_user(*, follower, following):
    if follower == following:
        raise ValidationError("Users cannot follow themselves.")

    follow, created = Follow.objects.get_or_create(
        follower=follower,
        following=following,
    )

    return follow, created


def unfollow_user(*, follower, following):
    deleted_count, _ = Follow.objects.filter(
        follower=follower,
        following=following,
    ).delete()

    return deleted_count > 0


def is_following(*, follower, following):
    return Follow.objects.filter(
        follower=follower,
        following=following,
    ).exists()