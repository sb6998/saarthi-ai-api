web: python manage.py runserver 0.0.0.0:$PORT
web: gunicorn saarthi.wsgi --log-file -
release: python manage.py migrate
