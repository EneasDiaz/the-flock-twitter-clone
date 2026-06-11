import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from likes.models import Like
from likes.services import has_liked, like_tweet, unlike_tweet
from tweets.models import Tweet


User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        email="user@example.com",
        username="testuser",
        display_name="Test User",
        password="VeryStrongPassword123!",
    )


@pytest.fixture
def tweet_author():
    return User.objects.create_user(
        email="author@example.com",
        username="author",
        display_name="Author User",
        password="VeryStrongPassword123!",
    )


@pytest.fixture
def tweet(tweet_author):
    return Tweet.objects.create(
        author=tweet_author,
        content="A tweet to like.",
    )


@pytest.mark.django_db
def test_create_like(user, tweet):
    like = Like.objects.create(user=user, tweet=tweet)

    assert like.user == user
    assert like.tweet == tweet
    assert str(like) == f"@testuser likes tweet {tweet.id}"


@pytest.mark.django_db
def test_user_can_like_tweet_only_once(user, tweet):
    Like.objects.create(user=user, tweet=tweet)

    with pytest.raises(IntegrityError):
        Like.objects.create(user=user, tweet=tweet)


@pytest.mark.django_db
def test_like_tweet_service_creates_like(user, tweet):
    like, created = like_tweet(user=user, tweet=tweet)

    assert created is True
    assert like.user == user
    assert like.tweet == tweet
    assert has_liked(user=user, tweet=tweet) is True


@pytest.mark.django_db
def test_like_tweet_service_does_not_duplicate_like(user, tweet):
    first_like, first_created = like_tweet(user=user, tweet=tweet)
    second_like, second_created = like_tweet(user=user, tweet=tweet)

    assert first_created is True
    assert second_created is False
    assert first_like.id == second_like.id
    assert Like.objects.count() == 1


@pytest.mark.django_db
def test_unlike_tweet_service_deletes_existing_like(user, tweet):
    Like.objects.create(user=user, tweet=tweet)

    deleted = unlike_tweet(user=user, tweet=tweet)

    assert deleted is True
    assert has_liked(user=user, tweet=tweet) is False


@pytest.mark.django_db
def test_unlike_tweet_service_returns_false_when_like_does_not_exist(user, tweet):
    deleted = unlike_tweet(user=user, tweet=tweet)

    assert deleted is False