# Task Manager API

A simple standalone FastAPI application for managing tasks with CRUD operations.

## Features

- Create, read, update, and delete tasks
- Task model: `uuid`, `title`, `description`, `status` (`created`, `in_progress`, `completed`)
- In-memory storage (no database required)
- OpenAPI/Swagger documentation at `/docs`
- Docker and docker-compose support
- Pytest-based test suite

## Quick Start

### 1. Run with Docker

```bash
docker-compose up --build
```

The API will be available at [http://localhost:8000](http://localhost:8000).

### 2. Run Locally

```bash
cd task_manager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. Run Tests

```bash
pytest
```

## API Documentation

Once running, visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive Swagger UI.

## Project Structure

```
task_manager/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── storage.py
│   ├── crud.py
│   └── routes.py
├── tests/
│   └── test_tasks.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## License

MIT
