FROM python:3.14.2-slim-trixie

LABEL maintainer="kumarswaraj"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV POETRY_VERSION=2.2.1
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

RUN addgroup --system django \
  && adduser --system \
  --no-create-home \
  --disabled-password \
  --ingroup django \
  django-user

COPY . .

RUN chown -R django-user:django /app \
  && chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]