# The Flock Twitter Clone

Full-stack Twitter/X clone built for **The Flock · Managed Software Teams** technical challenge.

The application includes custom authentication, tweets, timeline, follows, likes, search, seed data, responsive design, backend tests, coverage reporting, and Playwright end-to-end tests.

---

## Stack

* **Backend:** Django 5.2
* **Language:** Python 3.12
* **Database:** PostgreSQL 16
* **Frontend:** Django Templates with server-side rendering
* **Styling:** Custom mobile-first CSS
* **Testing:** pytest, pytest-django, coverage.py, Playwright
* **Infrastructure:** Docker and Docker Compose

---

## Why this stack

I chose Django because it provides a strong foundation for building a full-stack product quickly while keeping the architecture explicit and testable. It includes mature support for models, migrations, forms, sessions, authentication primitives, templating, and testing.

For this challenge, a server-rendered monolith was a pragmatic choice. It avoids unnecessary complexity around API authentication, CORS, duplicated frontend state, and separate deployments, while still allowing a complete user-facing product.

PostgreSQL was used as the relational database because the domain depends on relationships between users, tweets, follows, and likes. Docker Compose was added so evaluators can run the full stack with minimal setup.

---

# Runbook

## Prerequisites

The project was developed and tested with:

* Docker Desktop 29.5.3
* Docker Compose v5.1.4
* Python 3.12 inside the Docker container
* PostgreSQL 16 inside Docker
* Django 5.2.x

You do not need to install Python or PostgreSQL locally if you run the project with Docker.

---

## Environment variables

A `.env.example` file is included in the repository.

Create a local `.env` file:

```bash
cp .env.example .env
```

Required variables:

```env
DJANGO_SECRET_KEY=change-me-in-development
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

POSTGRES_DB=twitter_clone
POSTGRES_USER=twitter_clone
POSTGRES_PASSWORD=twitter_clone
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

Descriptions:

* `DJANGO_SECRET_KEY`: local Django secret key.
* `DJANGO_DEBUG`: enables or disables debug mode.
* `DJANGO_ALLOWED_HOSTS`: comma-separated list of allowed hosts.
* `POSTGRES_DB`: PostgreSQL database name.
* `POSTGRES_USER`: PostgreSQL username.
* `POSTGRES_PASSWORD`: PostgreSQL password.
* `POSTGRES_HOST`: database host. Use `db` when running with Docker Compose.
* `POSTGRES_PORT`: database port.

---

## Installation

Clone the repository:

```bash
git clone <REPOSITORY_URL>
cd the-flock-twitter-clone
```

Create the local environment file:

```bash
cp .env.example .env
```

Build the Docker image:

```bash
docker compose build
```

Run database migrations:

```bash
docker compose run --rm web python app/manage.py migrate
```

Run the seed data command:

```bash
docker compose run --rm web python app/manage.py seed_data
```

Start the application:

```bash
docker compose up
```

Open the app at:

```txt
http://localhost:8000
```

---

## Sample credentials

After running the seed command, you can log in with:

```txt
Email: demo@example.com
Password: VeryStrongPassword123!
```

All seeded users use the same password:

```txt
VeryStrongPassword123!
```

Example seeded users:

```txt
demo@example.com
alice@example.com
bob@example.com
carla@example.com
diego@example.com
```

---

## Running tests

Run the full test suite:

```bash
docker compose run --rm web pytest -q
```

Run backend tests only:

```bash
docker compose run --rm web pytest app -q
```

Run end-to-end tests only:

```bash
docker compose run --rm web pytest e2e -q
```

---

## Running coverage

Run coverage:

```bash
docker compose run --rm web coverage run -m pytest
```

Generate the report:

```bash
docker compose run --rm web coverage report
```

The backend test coverage is above 85%.

---

# Features

## Authentication

* User registration with email and password.
* Login and logout.
* Session-based authentication.
* Protected routes for authenticated actions.
* Custom user model with:

  * unique email
  * unique username
  * display name
  * bio
  * avatar placeholder color

Authentication is implemented using Django sessions and a custom user model. No third-party authentication provider is used.

---

## Tweets

Users can:

* create tweets
* write up to 280 characters
* delete their own tweets
* view tweets in a paginated timeline

Tweet validation is handled both at form level and model level.

---

## Timeline

The timeline shows:

* tweets created by the authenticated user
* tweets created by users they follow

Tweets are ordered from newest to oldest and paginated.

The current implementation uses a read-time query over the follows graph. This is simple, correct, and appropriate for the expected scale of the challenge. In a production-scale system, this could evolve into a materialized feed or fanout-on-write model.

---

## Follows graph

Users can:

* follow other users
* unfollow users
* view followers
* view following lists

The follow relationship is modeled with a dedicated `Follow` model.

Database constraints prevent:

* duplicate follow relationships
* users following themselves

---

## Likes

Users can:

* like tweets
* unlike tweets
* see visible like counters

The like relationship is modeled with a dedicated `Like` model.

A database constraint prevents the same user from liking the same tweet more than once.

---

## Search

Authenticated users can search for other users by:

* username
* display name

The search excludes the current user from the result list.

---

## Seed data

The project includes a custom Django management command:

```bash
python app/manage.py seed_data
```

It creates:

* 10 users
* tweets for each user
* follow relationships
* cross-likes
* sample login credentials

The command is idempotent, so it can be safely run more than once without duplicating data.

---

## Responsive design

The UI was built with a mobile-first approach.

Breakpoints:

* Mobile: below 640px
* Tablet: 640px to 1024px
* Desktop: above 1024px

The design is intentionally simple and focused on usability.

---

# Testing strategy

The test suite includes:

* model tests
* validation tests
* service tests
* integration tests for critical views
* authentication flow tests
* timeline tests
* follow and unfollow tests
* like and unlike tests
* search tests
* seed command tests
* Playwright end-to-end tests

Main E2E flows covered:

* user login
* tweet creation
* following another user and seeing their tweet in the timeline

---

# Technical decisions

## Custom authentication

A custom user model was created at the start of the project to avoid migration issues later. Email is used as the login identifier, while username remains unique and public-facing.

## Server-rendered frontend

I chose Django Templates instead of a separate JavaScript frontend to keep the product cohesive, reduce infrastructure overhead, and focus on correctness, testing, and delivery speed.

## Service layer

Some business logic was moved into service functions, especially for follows and likes. This keeps views simpler and makes core behavior easier to test.

## Database constraints

Important rules are enforced at database level where appropriate:

* unique follow relationship
* no self-follow
* unique like per user and tweet

This prevents invalid states even if application-level checks are bypassed.

## Docker

Docker Compose is used to run the application and PostgreSQL database together. This makes setup easier and reduces environment differences for evaluators.

---

# Known trade-offs and limitations

* The timeline is generated at read time. This is appropriate for the challenge, but a production-scale social network would likely use feed materialization.
* There is no real-time timeline update.
* Avatar support is currently a placeholder, not image upload.
* Replies and notifications were not implemented in order to prioritize required functionality, testing, documentation, and delivery quality.
* The UI is intentionally simple and functional rather than a pixel-perfect clone of Twitter/X.

---

# AI usage

AI tools were used throughout the development process to accelerate scaffolding, generate first-pass tests, review edge cases, and iterate on implementation details.

Generated code was manually reviewed, adjusted, tested, and committed progressively. The commit history reflects a feature-by-feature development process rather than a single generated code dump.

AI was especially useful for:

* breaking the challenge into implementation phases
* generating initial model, view, and test structures
* identifying missing validation cases
* improving the README and Runbook
* debugging Docker, Django, and Playwright issues

The final implementation decisions, fixes, test execution, and commits were reviewed manually.

---

# Useful commands

Build containers:

```bash
docker compose build
```

Start app:

```bash
docker compose up
```

Run migrations:

```bash
docker compose run --rm web python app/manage.py migrate
```

Seed data:

```bash
docker compose run --rm web python app/manage.py seed_data
```

Run tests:

```bash
docker compose run --rm web pytest -q
```

Run E2E tests:

```bash
docker compose run --rm web pytest e2e -q
```

Run coverage:

```bash
docker compose run --rm web coverage run -m pytest
docker compose run --rm web coverage report
```
