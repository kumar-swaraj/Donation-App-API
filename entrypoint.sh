#!/bin/sh
set -e

echo "🔧 Fixing media directory permissions..."
mkdir -p /app/media
chown -R django-user:django /app/media

echo "🔄 Waiting for PostgreSQL to become available..."
until python - <<EOF
import os
import psycopg

psycopg.connect(
    host=os.environ["DB_HOST"],
    dbname=os.environ["DB_NAME"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
)
EOF
do
  echo "⏳ Database not ready yet, retrying..."
  sleep 2
done

echo "✅ Database is ready"

if [ "${RUN_MIGRATIONS:-true}" = "true" ]; then
  echo "📦 Running migrations"
  python manage.py migrate --noinput
else
  echo "⏭️ Skipping migrations (RUN_MIGRATIONS=false)"
fi

echo "🚀 Starting application"
exec su django-user -s /bin/sh -c "$*"