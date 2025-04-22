FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry
COPY .env .env
COPY . .

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

EXPOSE 8080
 
CMD ["poetry", "run", "connexion-api"]