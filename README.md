# Docker Django Jinja Template

A Dockerized Django starter that renders templates with **Jinja2** instead of
the Django template language, backed by Postgres.

## Stack

- Django 6.1
- Jinja2 3.1 as the template backend
- PostgreSQL 17 (Compose service, with a healthcheck)
- psycopg 3
- gunicorn

## Getting started

```bash
cp .env.example .env

docker compose up --build
```

Compose waits for Postgres to pass its healthcheck, the entrypoint runs
`migrate`, and the dev server starts at http://localhost:8000

Without Docker:

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

## How Jinja2 is wired in

`root/jinja.py` defines the Jinja environment and exposes Django's `static`
and `url` (`reverse`) helpers as globals, so templates can call
`{{ static(...) }}` and `{{ url(...) }}` the same way Django templates do.
It is registered as a `Jinja2` backend in `settings.py`.

## Layout

```
root/                # project settings, urls, views, and jinja.py (Jinja environment)
templates/home.html  # example Jinja2 template
Dockerfile
docker-compose.yml   # web + Postgres services
entrypoint.sh        # waits for Postgres, then migrates
```

## Environment variables

See `.env.example`: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` and the
`POSTGRES_*` credentials.
