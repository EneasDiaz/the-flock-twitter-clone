import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from tweets.models import Tweet


User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        email="author@example.com",
        username="author",
        display_name="Author User",
        password="VeryStrongPassword123!",
    )


@pytest.mark.django_db
def test_create_tweet_with_author_and_content(user):
    tweet = Tweet.objects.create(
        author=user,
        content="This is my first tweet.",
    )

    assert tweet.author == user
    assert tweet.content == "This is my first tweet."
    assert tweet.created_at is not None
    assert tweet.updated_at is not None
    assert str(tweet) == "@author: This is my first tweet."


@pytest.mark.django_db
def test_tweet_content_max_length_is_280_characters(user):
    tweet = Tweet(
        author=user,
        content="x" * 280,
    )

    tweet.full_clean()

    assert tweet.content == "x" * 280


@pytest.mark.django_db
def test_tweet_content_cannot_exceed_280_characters(user):
    tweet = Tweet(
        author=user,
        content="x" * 281,
    )

    with pytest.raises(ValidationError):
        tweet.full_clean()


@pytest.mark.django_db
def test_tweet_content_cannot_be_blank(user):
    tweet = Tweet(
        author=user,
        content="",
    )

    with pytest.raises(ValidationError):
        tweet.full_clean()


@pytest.mark.django_db
def test_tweets_are_ordered_newest_first(user):
    older_tweet = Tweet.objects.create(
        author=user,
        content="Older tweet",
    )
    newer_tweet = Tweet.objects.create(
        author=user,
        content="Newer tweet",
    )

    tweets = list(Tweet.objects.all())

    assert tweets == [newer_tweet, older_tweet]


@pytest.mark.django_db
def test_tweets_are_deleted_when_author_is_deleted(user):
    Tweet.objects.create(
        author=user,
        content="This tweet should disappear.",
    )

    user.delete()

    assert Tweet.objects.count() == 0