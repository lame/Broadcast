web: gunicorn app:app  --worker-class gevent --preload --timeout 10
init: python manage.py db init
migrate: python manage.py db migrate
upgrade: python manage.py db upgrade
downgrade: python manage.py db downgrade
