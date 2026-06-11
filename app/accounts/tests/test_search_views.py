import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        email="user@example.com",
        username="currentuser",
        display_name="Current User",
        password="VeryStrongPassword123!",
    )


@pytest.fixture
def other_user():
    return User.objects.create_user(
        email="bob@example.com",
        username="bob",
        display_name="Bob Builder",
        bio="I build things.",
        password="VeryStrongPassword123!",
    )


@pytest.fixture
def third_user():
    return User.objects.create_user(
        email="alice@example.com",
        username="alice",
        display_name="Alice Runner",
        bio="I run a lot.",
        password="VeryStrongPassword123!",
    )


@pytest.mark.django_db
def test_search_requires_authentication(client):
    response = client.get(reverse("accounts:search"))

    assert response.status_code == 302
    assert response.url == f"{reverse('accounts:login')}?next={reverse('accounts:search')}"


@pytest.mark.django_db
def test_search_page_renders_for_authenticated_user(client, user):
    client.force_login(user)

    response = client.get(reverse("accounts:search"))

    assert response.status_code == 200
    assert b"Search users" in response.content
    assert b"Search for people by display name or username." in response.content


@pytest.mark.django_db
def test_search_finds_user_by_username(client, user, other_user):
    client.force_login(user)

    response = client.get(reverse("accounts:search"), {"q": "bob"})

    assert response.status_code == 200
    assert b"Bob Builder" in response.content
    assert b"@bob" in response.content


@pytest.mark.django_db
def test_search_finds_user_by_display_name(client, user, third_user):
    client.force_login(user)

    response = client.get(reverse("accounts:search"), {"q": "Runner"})

    assert response.status_code == 200
    assert b"Alice Runner" in response.content
    assert b"@alice" in response.content


@pytest.mark.django_db
def test_search_is_case_insensitive(client, user, other_user):
    client.force_login(user)

    response = client.get(reverse("accounts:search"), {"q": "BOB"})

    assert response.status_code == 200
    assert b"Bob Builder" in response.content


@pytest.mark.django_db
def test_search_excludes_current_user(client, user):
    client.force_login(user)

    response = client.get(reverse("accounts:search"), {"q": "currentuser"})

    assert response.status_code == 200
    assert b"Current User" not in response.content
    assert b"No users found." in response.content


@pytest.mark.django_db
def test_search_shows_no_users_found_when_no_match(client, user, other_user):
    client.force_login(user)

    response = client.get(reverse("accounts:search"), {"q": "nonexistent"})

    assert response.status_code == 200
    assert b"No users found." in response.content


@pytest.mark.django_db
def test_search_strips_empty_query(client, user, other_user):
    client.force_login(user)

    response = client.get(reverse("accounts:search"), {"q": "   "})

    assert response.status_code == 200
    assert b"Search for people by display name or username." in response.content
    assert b"Bob Builder" not in response.content