PORT ?= 8000

install:
	uv sync

lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix

db-up:
	docker compose -f __env__/dev/compose.yaml up --build -d

db-down:
	docker compose -f __env__/dev/compose.yaml down

db-logs:
	docker compose -f __env__/dev/compose.yaml logs -f

dev:
	uv run flask --debug --app page_analyzer:app run

start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	./build.sh

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
