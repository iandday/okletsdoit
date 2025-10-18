#!/bin/bash
set -e

# Activate virtual environment
export PATH="/app/.venv/bin:$PATH"

# Wait for database to be ready
echo "Waiting for database..."
while ! pg_isready -h ${POSTGRES_HOST:-localhost} -p ${POSTGRES_PORT:-5432} -U ${POSTGRES_USER:-okletsdoit}; do
    echo "Database is unavailable - sleeping"
    sleep 1
done
echo "Database is ready!"

if [[ ${CONTAINER_ROLE} == "beats" ]]; then
    rm -f ~/.celerybeat.pid
    /app/.venv/bin/celery -A okletsdoit.celery_app beat -l info

elif [[ ${CONTAINER_ROLE} == "worker" ]]; then
    /app/.venv/bin/celery -A okletsdoit.celery_app worker -l info
elif [[ ${CONTAINER_ROLE} == "server" ]]; then
    echo "Running database migrations..."
    /app/.venv/bin/python manage.py migrate --noinput

    echo "Collecting static files..."
    /app/.venv/bin/python manage.py collectstatic --noinput --clear

    echo "Configuring scheduled tasks..."
    /app/.venv/bin/python manage.py configure_tasks

    # Create superuser if it doesn't exist (optional, for production setup)
    if [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
        echo "Creating superuser..."
        /app/.venv/bin/python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='$DJANGO_SUPERUSER_EMAIL').exists():
    User.objects.create_superuser(
        email='$DJANGO_SUPERUSER_EMAIL',
        password='$DJANGO_SUPERUSER_PASSWORD',
        first_name='Admin',
        last_name='User'
    )
    print('Superuser created successfully')
else:
    print('Superuser already exists')
"
    fi

    if [[ ${LOCAL_DEV} == "True" ]]; then
        /app/.venv/bin/python manage.py runserver_plus 0.0.0.0:8000
    else
        /app/.venv/bin/gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 60 okletsdoit.wsgi:application 
    fi
else
    echo "Unknown CONTAINER_ROLE: $CONTAINER_ROLE"
    exit 1
fi