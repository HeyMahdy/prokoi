FROM python:3.13.3-slim


# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libssl-dev libffi-dev gcc curl && \
    rm -rf /var/lib/apt/lists/*

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

# Environment variables to disable virtualenv creation and enable non-interactive installs
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYTHONUNBUFFERED=1

# Regenerate poetry.lock and install dependencies
RUN poetry lock  && poetry install --no-root --no-interaction --no-ansi
RUN poetry install --no-root --no-interaction --no-ansi
COPY . /app

ENTRYPOINT ["poetry", "run", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]