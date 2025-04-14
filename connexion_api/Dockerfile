FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock README.md ./

COPY schema ./schema

COPY . /app



RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi



CMD ["poetry", "run", "connexion-api"]