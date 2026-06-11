import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from follows.models import Follow
from follows.services import follow_user, is_following, unfollow_user


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
def test_create_follow_relationship(user, other_user):
    follow = Follow.objects.create(follower=user, following=other_user)

    assert follow.follower == user
    assert follow.following == other_user
    assert str(follow) == "@testuser follows @otheruser"


@pytest.mark.django_db
def test_follow_relationship_must_be_unique(user, other_user):
    Follow.objects.create(follower=user, following=other_user)

    with pytest.raises(IntegrityError):
        Follow.objects.create(follower=user, following=other_user)


@pytest.mark.django_db
def test_user_cannot_follow_self_at_database_level(user):
    with pytest.raises(IntegrityError):
        Follow.objects.create(follower=user, following=user)


@pytest.mark.django_db
def test_follow_user_service_creates_relationship(user, other_user):
    follow, created = follow_user(follower=user, following=other_user)

    assert created is True
    assert follow.follower == user
    assert follow.following == other_user
    assert is_following(follower=user, following=other_user) is True


@pytest.mark.django_db
def test_follow_user_service_does_not_duplicate_relationship(user, other_user):
    first_follow, first_created = follow_user(follower=user, following=other_user)
    second_follow, second_created = follow_user(follower=user, following=other_user)

    assert first_created is True
    assert second_created is False
    assert first_follow.id == second_follow.id
    assert Follow.objects.count() == 1


@pytest.mark.django_db
def test_follow_user_service_prevents_self_follow(user):
    with pytest.raises(ValidationError):
        follow_user(follower=user, following=user)


@pytest.mark.django_db
def test_unfollow_user_service_deletes_existing_relationship(user, other_user):
    Follow.objects.create(follower=user, following=other_user)

    deleted = unfollow_user(follower=user, following=other_user)

    assert deleted is True
    assert is_following(follower=user, following=other_user) is False


@pytest.mark.django_db
def test_unfollow_user_service_returns_false_when_relationship_does_not_exist(user, other_user):
    deleted = unfollow_user(follower=user, following=other_user)

    assert deleted is False