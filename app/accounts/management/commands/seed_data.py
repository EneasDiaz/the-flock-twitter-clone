from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from follows.models import Follow
from likes.models import Like
from tweets.models import Tweet


User = get_user_model()

DEFAULT_PASSWORD = "VeryStrongPassword123!"


class Command(BaseCommand):
    help = "Seed the database with realistic users, tweets, follows, and likes."

    def handle(self, *args, **options):
        users_data = [
            {
                "email": "demo@example.com",
                "username": "demo",
                "display_name": "Demo User",
                "bio": "Testing the timeline, one tweet at a time.",
            },
            {
                "email": "alice@example.com",
                "username": "alice",
                "display_name": "Alice Runner",
                "bio": "Morning runs, coffee, and tiny product ideas.",
            },
            {
                "email": "bob@example.com",
                "username": "bob",
                "display_name": "Bob Builder",
                "bio": "I build things and occasionally tweet about it.",
            },
            {
                "email": "carla@example.com",
                "username": "carla",
                "display_name": "Carla Design",
                "bio": "Design systems, messy notebooks, clean interfaces.",
            },
            {
                "email": "diego@example.com",
                "username": "diego",
                "display_name": "Diego Dev",
                "bio": "Backend, mate, and questionable variable names.",
            },
            {
                "email": "emma@example.com",
                "username": "emma",
                "display_name": "Emma Product",
                "bio": "Turning vague ideas into slightly less vague roadmaps.",
            },
            {
                "email": "fran@example.com",
                "username": "fran",
                "display_name": "Fran Data",
                "bio": "Charts, queries, and strong opinions about dashboards.",
            },
            {
                "email": "gina@example.com",
                "username": "gina",
                "display_name": "Gina Mobile",
                "bio": "Mobile-first or it did not happen.",
            },
            {
                "email": "hugo@example.com",
                "username": "hugo",
                "display_name": "Hugo QA",
                "bio": "I break apps so users do not have to.",
            },
            {
                "email": "iris@example.com",
                "username": "iris",
                "display_name": "Iris Frontend",
                "bio": "CSS, components, and tiny layout victories.",
            },
        ]

        created_users = {}

        for user_data in users_data:
            user, _ = User.objects.get_or_create(
                email=user_data["email"],
                defaults={
                    "username": user_data["username"],
                    "display_name": user_data["display_name"],
                    "bio": user_data["bio"],
                },
            )

            user.username = user_data["username"]
            user.display_name = user_data["display_name"]
            user.bio = user_data["bio"]
            user.set_password(DEFAULT_PASSWORD)
            user.save()

            created_users[user.username] = user

        tweets_by_username = {
            "demo": [
                "First day testing this Twitter clone. Looks suspiciously productive.",
                "A good README is not documentation. It is hospitality.",
            ],
            "alice": [
                "Morning run done. Debugging my legs now.",
                "Hydration and pagination: both matter more than people think.",
            ],
            "bob": [
                "This is Bob tweet for the follow test.",
                "Built a tiny feature today. It only broke twice. Progress.",
            ],
            "carla": [
                "A button without spacing is just a cry for help.",
                "Mobile-first design saves you from desktop-first regret.",
            ],
            "diego": [
                "Database constraints are love letters to future maintainers.",
                "The best bug is the one covered by a regression test.",
            ],
            "emma": [
                "Scope is a feature. Especially with a 72-hour deadline.",
                "Shipping small, coherent increments beats heroic chaos.",
            ],
            "fran": [
                "If the metric needs a 40-slide explanation, maybe it is not the metric.",
                "Data without context is just numbers wearing a trench coat.",
            ],
            "gina": [
                "Tested the app on mobile. My thumb has feedback.",
                "Responsive design is not a breakpoint collection hobby.",
            ],
            "hugo": [
                "QA note: users will click the thing you forgot existed.",
                "If it only works on your machine, congratulations on your local startup.",
            ],
            "iris": [
                "CSS did exactly what I asked, not what I meant. Again.",
                "Small UI polish makes features feel less haunted.",
            ],
        }

        created_tweets = []

        for username, contents in tweets_by_username.items():
            author = created_users[username]

            for content in contents:
                tweet, _ = Tweet.objects.get_or_create(
                    author=author,
                    content=content,
                )
                created_tweets.append(tweet)

        follow_pairs = [
            ("demo", "alice"),
            ("demo", "bob"),
            ("demo", "carla"),
            ("alice", "bob"),
            ("alice", "gina"),
            ("bob", "diego"),
            ("bob", "hugo"),
            ("carla", "iris"),
            ("diego", "fran"),
            ("emma", "demo"),
            ("fran", "emma"),
            ("gina", "carla"),
            ("hugo", "diego"),
            ("iris", "carla"),
            ("iris", "gina"),
        ]

        for follower_username, following_username in follow_pairs:
            Follow.objects.get_or_create(
                follower=created_users[follower_username],
                following=created_users[following_username],
            )

        like_pairs = [
            ("demo", "bob"),
            ("demo", "carla"),
            ("alice", "bob"),
            ("alice", "diego"),
            ("bob", "alice"),
            ("carla", "iris"),
            ("diego", "fran"),
            ("emma", "demo"),
            ("fran", "emma"),
            ("gina", "carla"),
            ("hugo", "diego"),
            ("iris", "gina"),
        ]

        for liker_username, author_username in like_pairs:
            liker = created_users[liker_username]
            author = created_users[author_username]
            author_tweets = Tweet.objects.filter(author=author)

            for tweet in author_tweets[:1]:
                Like.objects.get_or_create(
                    user=liker,
                    tweet=tweet,
                )

        self.stdout.write(self.style.SUCCESS("Seed data created successfully."))
        self.stdout.write(
            self.style.SUCCESS(
                f"Sample login: demo@example.com / {DEFAULT_PASSWORD}"
            )
        )