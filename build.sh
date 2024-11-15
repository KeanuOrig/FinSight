#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install --upgrade pip && pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

# Create superuser with environment variables if it doesn't already exist
python manage.py shell -c "
from django.contrib.auth import get_user_model;
import os;
User = get_user_model();
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin');
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@admin.com');
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin');
User.objects.create_superuser(username, email, password) if not User.objects.filter(username=username).exists() else None
"