import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command

from follows.models import Follow
from likes.models import Like
from tweets.models import Tweet


User = get_user_model()


@pytest.mark.django_db
def test_seed_data_command_creates_demo_content():
    call_command("seed_data")

    assert User.objects.count() == 10
    assert Tweet.objects.count() == 20
    assert Follow.objects.count() == 15
    assert Like.objects.count() == 12

    demo = User.objects.get(email="demo@example.com")

    assert demo.username == "demo"
    assert demo.display_name == "Demo User"
    assert demo.check_password("VeryStrongPassword123!") is True


@pytest.mark.django_db
def test_seed_data_command_is_idempotent():
    call_command("seed_data")
    call_command("seed_data")

    assert User.objects.count() == 10
    assert Tweet.objects.count() == 20
    assert Follow.objects.count() == 15
    assert Like.objects.count() == 12