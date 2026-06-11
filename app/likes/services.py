from .models import Like


def like_tweet(*, user, tweet):
    like, created = Like.objects.get_or_create(
        user=user,
        tweet=tweet,
    )

    return like, created


def unlike_tweet(*, user, tweet):
    deleted_count, _ = Like.objects.filter(
        user=user,
        tweet=tweet,
    ).delete()

    return deleted_count > 0


def has_liked(*, user, tweet):
    return Like.objects.filter(
        user=user,
        tweet=tweet,
    ).exists()