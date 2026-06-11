import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

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
def other_user():
    return User.objects.create_user(
        email="other@example.com",
        username="otheruser",
        display_name="Other User",
        password="VeryStrongPassword123!",
    )


@pytest.mark.django_db
def test_timeline_requires_authentication(client):
    response = client.get(reverse("tweets:timeline"))

    assert response.status_code == 302
    assert response.url == f"{reverse('accounts:login')}?next={reverse('tweets:timeline')}"


@pytest.mark.django_db
def test_authenticated_user_can_view_timeline(client, user):
    client.force_login(user)

    response = client.get(reverse("tweets:timeline"))

    assert response.status_code == 200
    assert b"Timeline" in response.content
    assert b"Latest tweets" in response.content


@pytest.mark.django_db
def test_timeline_shows_current_user_tweets(client, user):
    Tweet.objects.create(author=user, content="Hello from my timeline.")
    client.force_login(user)

    response = client.get(reverse("tweets:timeline"))

    assert response.status_code == 200
    assert b"Hello from my timeline." in response.content
    assert b"@testuser" in response.content


@pytest.mark.django_db
def test_user_can_create_tweet(client, user):
    client.force_login(user)

    response = client.post(
        reverse("tweets:create"),
        {"content": "This is a valid tweet."},
    )

    tweet = Tweet.objects.get(author=user)

    assert response.status_code == 302
    assert response.url == reverse("tweets:timeline")
    assert tweet.content == "This is a valid tweet."


@pytest.mark.django_db
def test_create_tweet_requires_authentication(client):
    response = client.post(
        reverse("tweets:create"),
        {"content": "Anonymous tweet attempt."},
    )

    assert response.status_code == 302
    assert response.url == f"{reverse('accounts:login')}?next={reverse('tweets:create')}"
    assert Tweet.objects.count() == 0


@pytest.mark.django_db
def test_user_cannot_create_blank_tweet(client, user):
    client.force_login(user)

    response = client.post(
        reverse("tweets:create"),
        {"content": "   "},
    )

    assert response.status_code == 302
    assert response.url == reverse("tweets:timeline")
    assert Tweet.objects.count() == 0


@pytest.mark.django_db
def test_user_cannot_create_tweet_longer_than_280_characters(client, user):
    client.force_login(user)

    response = client.post(
        reverse("tweets:create"),
        {"content": "x" * 281},
    )

    assert response.status_code == 302
    assert response.url == reverse("tweets:timeline")
    assert Tweet.objects.count() == 0


@pytest.mark.django_db
def test_user_can_delete_own_tweet(client, user):
    tweet = Tweet.objects.create(author=user, content="Delete me.")
    client.force_login(user)

    response = client.post(reverse("tweets:delete", args=[tweet.id]))

    assert response.status_code == 302
    assert response.url == reverse("tweets:timeline")
    assert Tweet.objects.filter(id=tweet.id).exists() is False


@pytest.mark.django_db
def test_user_cannot_delete_another_users_tweet(client, user, other_user):
    tweet = Tweet.objects.create(author=other_user, content="You cannot delete me.")
    client.force_login(user)

    response = client.post(reverse("tweets:delete", args=[tweet.id]))

    assert response.status_code == 404
    assert Tweet.objects.filter(id=tweet.id).exists() is True


@pytest.mark.django_db
def test_timeline_is_paginated(client, user):
    for index in range(12):
        Tweet.objects.create(author=user, content=f"Tweet number {index}")

    client.force_login(user)

    response = client.get(reverse("tweets:timeline"))

    assert response.status_code == 200
    assert len(response.context["page_obj"]) == 10
    assert response.context["page_obj"].has_next() is True