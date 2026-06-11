import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError


User = get_user_model()


@pytest.mark.django_db
def test_create_user_with_email_username_display_name_and_password():
    user = User.objects.create_user(
        email="user@example.com",
        username="testuser",
        display_name="Test User",
        password="strong-password-123",
    )

    assert user.email == "user@example.com"
    assert user.username == "testuser"
    assert user.display_name == "Test User"
    assert user.check_password("strong-password-123")
    assert str(user) == "@testuser"
    assert user.is_staff is False
    assert user.is_superuser is False


@pytest.mark.django_db
def test_create_user_requires_email():
    with pytest.raises(ValueError, match="email"):
        User.objects.create_user(
            email="",
            username="testuser",
            display_name="Test User",
            password="strong-password-123",
        )


@pytest.mark.django_db
def test_user_email_must_be_unique():
    User.objects.create_user(
        email="same@example.com",
        username="userone",
        display_name="User One",
        password="strong-password-123",
    )

    with pytest.raises(IntegrityError):
        User.objects.create_user(
            email="same@example.com",
            username="usertwo",
            display_name="User Two",
            password="strong-password-123",
        )


@pytest.mark.django_db
def test_username_must_be_unique():
    User.objects.create_user(
        email="one@example.com",
        username="sameusername",
        display_name="User One",
        password="strong-password-123",
    )

    with pytest.raises(IntegrityError):
        User.objects.create_user(
            email="two@example.com",
            username="sameusername",
            display_name="User Two",
            password="strong-password-123",
        )


@pytest.mark.django_db
def test_bio_max_length_is_validated():
    user = User(
        email="bio@example.com",
        username="biouser",
        display_name="Bio User",
        bio="x" * 161,
    )

    with pytest.raises(ValidationError):
        user.full_clean()


@pytest.mark.django_db
def test_create_superuser_sets_required_flags():
    admin = User.objects.create_superuser(
        email="admin@example.com",
        username="admin",
        display_name="Admin User",
        password="admin-password-123",
    )

    assert admin.is_staff is True
    assert admin.is_superuser is True
    assert admin.is_active is True


@pytest.mark.django_db
def test_create_superuser_requires_staff_flag():
    with pytest.raises(ValueError, match="is_staff=True"):
        User.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            display_name="Admin User",
            password="admin-password-123",
            is_staff=False,
        )


@pytest.mark.django_db
def test_create_superuser_requires_superuser_flag():
    with pytest.raises(ValueError, match="is_superuser=True"):
        User.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            display_name="Admin User",
            password="admin-password-123",
            is_superuser=False,
        )