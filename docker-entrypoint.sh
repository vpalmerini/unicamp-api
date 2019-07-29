#!/bin/sh
create_superuser="
import django
django.setup()
from django.contrib.auth.models import User
from django.db import IntegrityError
try:
    User.objects.create_superuser('$SUPERUSER_NAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD', first_name='admin', last_name='1')
    print('Superuser \'$SUPERUSER_NAME\' created')
except IntegrityError:
    print('Superuser \'$SUPERUSER_NAME\' already exists')
except Exception as e:
    print(e)
"
create_superuser() {
    if [ -z "$SUPERUSER_NAME" ] || [ -z "$SUPERUSER_EMAIL" ] || [ -z "$SUPERUSER_PASSWORD" ]; then
        echo "Environment variables for database not set, not creating superuser."
    else
        echo "Creating superuser"
        python -c "$create_superuser"
    fi
}

echo "Making migrations"
# Make database migrations
python manage.py makemigrations
python manage.py makemigrations institutes courses subjects classes professors

echo "Running migrations"
# Apply database migrations
python manage.py migrate

# run the function above
create_superuser

# run scripts to populate the db
python manage.py runscript create_institutes
python manage.py runscript create_courses
python manage.py runscript create_subjects
python manage.py runscript create_classes
python manage.py runscript create_professors


echo "Executing CMD"
exec "$@"
