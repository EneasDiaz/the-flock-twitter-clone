import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


@pytest.mark.django_db
def test_register_page_renders(client):
    response = client.get(reverse("accounts:register"))

    assert response.status_code == 200
    assert b"Create your account" in response.content


@pytest.mark.django_db
def test_user_can_register_and_is_logged_in(client):
    response = client.post(
        reverse("accounts:register"),
        {
            "email": "newuser@example.com",
            "username": "newuser",
            "display_name": "New User",
            "bio": "Hello world",
            "password1": "VeryStrongPassword123!",
            "password2": "VeryStrongPassword123!",
        },
    )

    user = User.objects.get(email="newuser@example.com")

    assert response.status_code == 302
    assert response.url == reverse("accounts:profile")
    assert user.username == "newuser"
    assert user.display_name == "New User"
    assert user.bio == "Hello world"
    assert str(user.id) == client.session["_auth_user_id"]


@pytest.mark.django_db
def test_authenticated_user_is_redirected_from_register_to_profile(client):
    user = User.objects.create_user(
        email="user@example.com",
        username="testuser",
        display_name="Test User",
        password="VeryStrongPassword123!",
    )
    client.force_login(user)

    response = client.get(reverse("accounts:register"))

    assert response.status_code == 302
    assert response.url == reverse("accounts:profile")


@pytest.mark.django_db
def test_login_page_renders(client):
    response = client.get(reverse("accounts:login"))

    assert response.status_code == 200
    assert b"Login" in response.content


@pytest.mark.django_db
def test_user_can_login_with_email_and_password(client):
    user = User.objects.create_user(
        email="login@example.com",
        username="loginuser",
        display_name="Login User",
        password="VeryStrongPassword123!",
    )

    response = client.post(
        reverse("accounts:login"),
        {
            "username": "login@example.com",
            "password": "VeryStrongPassword123!",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("accounts:profile")
    assert str(user.id) == client.session["_auth_user_id"]


@pytest.mark.django_db
def test_user_can_logout(client):
    user = User.objects.create_user(
        email="logout@example.com",
        username="logoutuser",
        display_name="Logout User",
        password="VeryStrongPassword123!",
    )
    client.force_login(user)

    response = client.post(reverse("accounts:logout"))

    assert response.status_code == 302
    assert response.url == reverse("accounts:login")
    assert "_auth_user_id" not in client.session


@pytest.mark.django_db
def test_profile_requires_authentication(client):
    response = client.get(reverse("accounts:profile"))

    assert response.status_code == 302
    assert response.url == f"{reverse('accounts:login')}?next={reverse('accounts:profile')}"


@pytest.mark.django_db
def test_authenticated_user_can_view_profile(client):
    user = User.objects.create_user(
        email="profile@example.com",
        username="profileuser",
        display_name="Profile User",
        bio="This is my bio",
        password="VeryStrongPassword123!",
    )
    client.force_login(user)

    response = client.get(reverse("accounts:profile"))

    assert response.status_code == 200
    assert b"Profile User" in response.content
    assert b"@profileuser" in response.content
    assert b"This is my bio" in response.content