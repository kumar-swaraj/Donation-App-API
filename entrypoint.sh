#!/bin/sh
set -e

echo "🏁 Booting Django container"

# -------------------------
# Hard fail on bad config
# -------------------------
: "${DJANGO_SETTINGS_MODULE:?DJANGO_SETTINGS_MODULE is required}"
: "${DJANGO_SECRET_KEY:?DJANGO_SECRET_KEY is required}"
: "${DB_HOST:?DB_HOST is required}"
: "${DB_NAME:?DB_NAME is required}"
: "${DB_USER:?DB_USER is required}"
: "${DB_PASSWORD:?DB_PASSWORD is required}"

echo "⚙️  DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE"

# -------------------------
# Filesystem prep
# -------------------------
mkdir -p /app/media
chown -R django-user:django /app/media

# -------------------------
# Wait for PostgreSQL (with timeout)
# -------------------------
echo "🔄 Waiting for PostgreSQL..."
ATTEMPTS=30

until python - <<EOF
import os, psycopg
psycopg.connect(
    host=os.environ["DB_HOST"],
    dbname=os.environ["DB_NAME"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
)
EOF
do
  ATTEMPTS=$((ATTEMPTS - 1))
  if [ "$ATTEMPTS" -le 0 ]; then
    echo "❌ Database never became available"
    exit 1
  fi
  sleep 2
done

echo "✅ Database is ready"

run_as_django() {
  su django-user -s /bin/sh -c "$1"
}

# -------------------------
# Migrations
# -------------------------
if [ "${RUN_MIGRATIONS:-true}" = "true" ]; then
  echo "📦 Running migrations"
  run_as_django "python manage.py migrate --noinput"
else
  echo "⏭️  Skipping migrations"
fi

# -------------------------
# Collect static files
# -------------------------
if [ "${RUN_COLLECTSTATIC:-true}" = "true" ]; then
  echo "🎨 Running collectstatic"
  run_as_django "python manage.py collectstatic --noinput"
else
  echo "⏭️  Skipping collectstatic"
fi

# -------------------------
# Start application
# -------------------------
echo "🚀 Executing command: $*"
exec su django-user -s /bin/sh -c "$*"