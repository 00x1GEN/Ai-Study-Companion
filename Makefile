.PHONY: up down logs test backend-test seed migrate lint

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f backend

test:
	docker compose run --rm backend sh -lc 'alembic upgrade head && python -m app.seed && pytest -q'

backend-test:
	cd backend && pytest -q

migrate:
	docker compose run --rm backend alembic upgrade head

seed:
	docker compose run --rm backend python -m app.seed

lint:
	cd backend && ruff check app tests
