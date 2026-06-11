import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from likes.models import Like
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
        content="This tweet can be liked.",
    )


@pytest.mark.django_db
def test_like_requires_authentication(client, tweet):
    response = client.post(reverse("likes:like", args=[tweet.id]))

    assert response.status_code == 302
    assert response.url == f"{reverse('accounts:login')}?next={reverse('likes:like', args=[tweet.id])}"
    assert Like.objects.count() == 0


@pytest.mark.django_db
def test_authenticated_user_can_like_tweet(client, user, tweet):
    client.force_login(user)

    response = client.post(reverse("likes:like", args=[tweet.id]))

    assert response.status_code == 302
    assert response.url == reverse("tweets:timeline")
    assert Like.objects.filter(user=user, tweet=tweet).exists() is True


@pytest.mark.django_db
def test_authenticated_user_can_unlike_tweet(client, user, tweet):
    Like.objects.create(user=user, tweet=tweet)
    client.force_login(user)

    response = client.post(reverse("likes:unlike", args=[tweet.id]))

    assert response.status_code == 302
    assert response.url == reverse("tweets:timeline")
    assert Like.objects.filter(user=user, tweet=tweet).exists() is False


@pytest.mark.django_db
def test_like_view_does_not_duplicate_likes(client, user, tweet):
    client.force_login(user)

    client.post(reverse("likes:like", args=[tweet.id]))
    client.post(reverse("likes:like", args=[tweet.id]))

    assert Like.objects.filter(user=user, tweet=tweet).count() == 1


@pytest.mark.django_db
def test_timeline_shows_like_counter(client, user):
    tweet = Tweet.objects.create(author=user, content="Tweet with likes.")
    Like.objects.create(user=user, tweet=tweet)

    client.force_login(user)

    response = client.get(reverse("tweets:timeline"))

    assert response.status_code == 200
    assert b"Tweet with likes." in response.content
    assert b"1 likes" in response.content


@pytest.mark.django_db
def test_timeline_shows_unlike_button_for_liked_tweet(client, user):
    tweet = Tweet.objects.create(author=user, content="Already liked tweet.")
    Like.objects.create(user=user, tweet=tweet)

    client.force_login(user)

    response = client.get(reverse("tweets:timeline"))

    assert response.status_code == 200
    assert b"Unlike" in response.content


@pytest.mark.django_db
def test_timeline_shows_like_button_for_unliked_tweet(client, user):
    Tweet.objects.create(author=user, content="Not liked yet.")

    client.force_login(user)

    response = client.get(reverse("tweets:timeline"))

    assert response.status_code == 200
    assert b"Like" in response.content