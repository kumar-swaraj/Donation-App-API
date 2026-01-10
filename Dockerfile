FROM python:3.14.2-slim-trixie

LABEL maintainer="kumarswaraj"

# ----------------------------------------
# Runtime behavior
# ----------------------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ----------------------------------------
# Install Poetry
# ----------------------------------------
ENV POETRY_VERSION=2.2.1
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# ----------------------------------------
# App directory
# ----------------------------------------
WORKDIR /app

# ----------------------------------------
# Install dependencies (cached layer)
# ----------------------------------------
COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# ----------------------------------------
# Copy application code
# ----------------------------------------
COPY . .

# ----------------------------------------
# Create non-root service user
# ----------------------------------------
RUN addgroup --system django \
  && adduser --system \
  --no-create-home \
  --disabled-password \
  --ingroup django \
  django-user \
  && chown -R django-user:django /app \
  && chmod +x /app/entrypoint.sh

# ----------------------------------------
# Drop privileges
# ----------------------------------------
USER django-user

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]