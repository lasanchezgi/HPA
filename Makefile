.PHONY: up down logs migrate test lint format shell build

# ── Docker ────────────────────────────────────────────────────────────────────
up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f api

shell:
	docker compose exec api bash

# ── Database ──────────────────────────────────────────────────────────────────
migrate:
	docker compose exec api alembic upgrade head

migration:
	docker compose exec api alembic revision --autogenerate -m "$(name)"

downgrade:
	docker compose exec api alembic downgrade -1

# ── Tests ─────────────────────────────────────────────────────────────────────
test:
	docker compose exec api pytest --cov=src --cov-report=term-missing -q

test-unit:
	docker compose exec api pytest tests/unit -q

test-integration:
	docker compose exec api pytest tests/integration -q

# ── Code quality ──────────────────────────────────────────────────────────────
lint:
	docker compose exec api ruff check src tests
	docker compose exec api mypy src

format:
	docker compose exec api ruff format src tests
	docker compose exec api ruff check --fix src tests

# ── Local (no Docker) ─────────────────────────────────────────────────────────
install:
	pip install -e "backend/.[dev]"
	pre-commit install

local-test:
	cd backend && pytest --cov=src --cov-report=term-missing -q

local-lint:
	cd backend && ruff check src tests && mypy src

local-format:
	cd backend && ruff format src tests && ruff check --fix src tests
