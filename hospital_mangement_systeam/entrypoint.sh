#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Start the Django development server
exec "$@"