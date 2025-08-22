venv-init:
	uv venv .venv --python=python3.12.11

freeze:
	uv pip freeze > requirements.txt

install:
	uv pip freeze -r requirements.txt

docker-build:
	docker compose up --build -d

alembic-revision:
	alembic revision --autogenerate -m "$(m)"

alembic-upgrade:
	alembic upgrade head


run:
	uv run main.py

client-run:
	uv run -m src.api.v1.client.task_client