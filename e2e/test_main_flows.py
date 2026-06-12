import os

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import connections
from playwright.sync_api import expect, sync_playwright

from follows.models import Follow
from tweets.models import Tweet


User = get_user_model()


@pytest.fixture
def page():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True,
            args=["--no-sandbox"],
        )
        page = browser.new_page(
            viewport={
                "width": 390,
                "height": 844,
            }
        )

        yield page

        page.close()
        browser.close()
        connections.close_all()


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


def login(page, live_server, email, password):
    page.goto(f"{live_server.url}{reverse('accounts:login')}")
    page.fill("input[name='username']", email)
    page.fill("input[name='password']", password)
    page.click("button[type='submit']")


@pytest.mark.django_db(transaction=True)
def test_user_can_login(live_server, page, user):
    login(
        page,
        live_server,
        "user@example.com",
        "VeryStrongPassword123!",
    )

    expect(page).to_have_url(f"{live_server.url}{reverse('tweets:timeline')}")
    expect(page.get_by_role("heading", name="Timeline")).to_be_visible()


@pytest.mark.django_db(transaction=True)
def test_user_can_create_tweet_from_timeline(live_server, page, user):
    login(
        page,
        live_server,
        "user@example.com",
        "VeryStrongPassword123!",
    )

    page.fill("textarea[name='content']", "Tweet created from an E2E test.")
    page.get_by_role("button", name="Tweet").click()

    expect(page).to_have_url(f"{live_server.url}{reverse('tweets:timeline')}")
    expect(page.get_by_text("Tweet created from an E2E test.")).to_be_visible()

    assert Tweet.objects.filter(
        author=user,
        content="Tweet created from an E2E test.",
    ).exists()


@pytest.mark.django_db(transaction=True)
def test_user_can_follow_another_user(live_server, page, user, other_user):
    Tweet.objects.create(
        author=other_user,
        content="Tweet from user followed in E2E test.",
    )

    login(
        page,
        live_server,
        "user@example.com",
        "VeryStrongPassword123!",
    )

    page.goto(f"{live_server.url}{reverse('accounts:profile_detail', args=[other_user.username])}")
    page.get_by_role("button", name="Follow").click()

    expect(page).to_have_url(
        f"{live_server.url}{reverse('accounts:profile_detail', args=[other_user.username])}"
    )
    expect(page.get_by_role("button", name="Unfollow")).to_be_visible()

    assert Follow.objects.filter(
        follower=user,
        following=other_user,
    ).exists()

    page.goto(f"{live_server.url}{reverse('tweets:timeline')}")
    expect(page.get_by_text("Tweet from user followed in E2E test.")).to_be_visible()