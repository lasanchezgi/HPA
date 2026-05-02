# Habit Power App

[![CI](https://github.com/lasanchezgi/HPA/actions/workflows/ci.yml/badge.svg)](https://github.com/lasanchezgi/HPA/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/lasanchezgi/HPA/branch/main/graph/badge.svg)](https://codecov.io/gh/lasanchezgi/HPA)

Track daily habits, build streaks, earn rewards, and predict your success.

## Architecture

Clean Architecture with strict layer separation:

```
domain/        — pure Python dataclasses and ABCs, zero framework imports
application/   — use cases that orchestrate domain logic
infrastructure — SQLAlchemy models, Postgres repos, JWT/bcrypt
delivery/      — FastAPI routers, Pydantic schemas, DI wiring
```

## Quick start

```bash
cp .env.example .env          # review and adjust secrets
make up                        # start api + postgres + redis
make migrate                   # apply migrations
```

API docs available at http://localhost:8000/docs

## Development

```bash
make install       # install deps + pre-commit hooks (local)
make logs          # tail api logs
make shell         # bash inside the api container
make test          # run full test suite with coverage
make lint          # ruff + mypy
make format        # auto-fix style issues
```

### Creating a new migration

```bash
make migration name="add_user_timezone"
make migrate
```

## API endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/v1/auth/register` | — | Register a new user |
| POST | `/api/v1/auth/login` | — | Get JWT access token |
| GET | `/api/v1/habits/` | JWT | List your habits |
| POST | `/api/v1/habits/` | JWT | Create a habit |
| GET | `/api/v1/habits/{id}` | JWT | Get habit detail |
| POST | `/api/v1/habits/{id}/log` | JWT | Log a completion |
| GET | `/api/v1/dashboard/summary` | JWT | Dashboard summary |
| GET | `/health` | — | Health check |

## Project structure

```
habit-power-app/
├── backend/
│   ├── src/
│   │   ├── domain/          # entities, value objects, repo interfaces
│   │   ├── application/     # use cases + DTOs
│   │   ├── infrastructure/  # SQLAlchemy, Postgres repos, security
│   │   └── delivery/        # FastAPI routes, schemas, DI
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   ├── alembic/
│   ├── main.py
│   ├── config.py
│   └── Dockerfile
├── docker-compose.yml
├── docker-compose.override.yml
├── Makefile
└── .env.example
```

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | postgres://... | Async PostgreSQL URL |
| `SECRET_KEY` | — | JWT signing secret (change in prod!) |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token lifetime |
| `ENVIRONMENT` | `development` | `development` or `production` |
| `REDIS_URL` | redis://... | Redis connection URL |
