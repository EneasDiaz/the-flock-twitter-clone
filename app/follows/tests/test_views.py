import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from follows.models import Follow
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
        bio="Other user's bio",
        password="VeryStrongPassword123!",
    )


@pytest.mark.django_db
def test_follow_requires_authentication(client, other_user):
    response = client.post(reverse("follows:follow", args=[other_user.username]))

    assert response.status_code == 302
    assert response.url == (
        f"{reverse('accounts:login')}?next="
        f"{reverse('follows:follow', args=[other_user.username])}"
    )
    assert Follow.objects.count() == 0


@pytest.mark.django_db
def test_authenticated_user_can_follow_another_user(client, user, other_user):
    client.force_login(user)

    response = client.post(reverse("follows:follow", args=[other_user.username]))

    assert response.status_code == 302
    assert response.url == reverse("accounts:profile_detail", args=[other_user.username])
    assert Follow.objects.filter(follower=user, following=other_user).exists() is True


@pytest.mark.django_db
def test_authenticated_user_can_unfollow_another_user(client, user, other_user):
    Follow.objects.create(follower=user, following=other_user)
    client.force_login(user)

    response = client.post(reverse("follows:unfollow", args=[other_user.username]))

    assert response.status_code == 302
    assert response.url == reverse("accounts:profile_detail", args=[other_user.username])
    assert Follow.objects.filter(follower=user, following=other_user).exists() is False


@pytest.mark.django_db
def test_user_cannot_follow_self_from_view(client, user):
    client.force_login(user)

    response = client.post(reverse("follows:follow", args=[user.username]))

    assert response.status_code == 302
    assert response.url == reverse("accounts:profile_detail", args=[user.username])
    assert Follow.objects.count() == 0


@pytest.mark.django_db
def test_profile_detail_shows_follow_button_when_not_following(client, user, other_user):
    client.force_login(user)

    response = client.get(reverse("accounts:profile_detail", args=[other_user.username]))

    assert response.status_code == 200
    assert b"Other User" in response.content
    assert b"@otheruser" in response.content
    assert b"Follow" in response.content


@pytest.mark.django_db
def test_profile_detail_shows_unfollow_button_when_following(client, user, other_user):
    Follow.objects.create(follower=user, following=other_user)
    client.force_login(user)

    response = client.get(reverse("accounts:profile_detail", args=[other_user.username]))

    assert response.status_code == 200
    assert b"Unfollow" in response.content


@pytest.mark.django_db
def test_followers_list_shows_users_who_follow_profile(client, user, other_user):
    Follow.objects.create(follower=user, following=other_user)
    client.force_login(user)

    response = client.get(reverse("accounts:followers_list", args=[other_user.username]))

    assert response.status_code == 200
    assert b"Followers of @otheruser" in response.content
    assert b"@testuser" in response.content


@pytest.mark.django_db
def test_following_list_shows_users_profile_is_following(client, user, other_user):
    Follow.objects.create(follower=user, following=other_user)
    client.force_login(user)

    response = client.get(reverse("accounts:following_list", args=[user.username]))

    assert response.status_code == 200
    assert b"Following of @testuser" in response.content
    assert b"@otheruser" in response.content


@pytest.mark.django_db
def test_timeline_shows_tweets_from_followed_users(client, user, other_user):
    Follow.objects.create(follower=user, following=other_user)
    Tweet.objects.create(author=other_user, content="Tweet from followed user.")
    client.force_login(user)

    response = client.get(reverse("tweets:timeline"))

    assert response.status_code == 200
    assert b"Tweet from followed user." in response.content
    assert b"@otheruser" in response.content


@pytest.mark.django_db
def test_timeline_does_not_show_tweets_from_unfollowed_users(client, user, other_user):
    Tweet.objects.create(author=other_user, content="Tweet from unfollowed user.")
    client.force_login(user)

    response = client.get(reverse("tweets:timeline"))

    assert response.status_code == 200
    assert b"Tweet from unfollowed user." not in response.content
    