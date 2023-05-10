#!/bin/sh
python manage.py runserver 0.0.0.0:8000 &
celery -A livis.celery worker --loglevel=info &
python /root/freedom/backend/LIVIS/livis/annotate/extract -m http.server 3306 &
