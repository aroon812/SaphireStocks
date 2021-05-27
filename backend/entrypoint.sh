#!/bin/sh
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do 
        sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py collectstatic --nooutput
python manage.py migrate --noinput
echo "from django.contrib.auth.models import User;
from django.contrib.auth import get_user_model;
get_user_model().objects.filter(email='$DJANGO_ADMIN_EMAIL').delete();
get_user_model().objects.create_superuser('$DJANGO_ADMIN_USER', '$DJANGO_ADMIN_EMAIL', '$DJANGO_ADMIN_PASSWORD')" | python manage.py shell

exec "$@"