django-migrate:
	./manage.py migrate --fake movies 0001
	./manage.py migrate
sqlite-load:
	python3 sqlite_to_postgres/load_data.py

start:
	./manage.py runserver

admin:
	DJANGO_SUPERUSER_USERNAME=admin \
	DJANGO_SUPERUSER_PASSWORD=123 \
	DJANGO_SUPERUSER_EMAIL=123@123.ru \
	python manage.py createsuperuser --noinput || true

make-trans:
	django-admin makemessages --ignore venv -l en -l ru
compile-trans:
	django-admin compilemessages -l en -l ru --exclude venv
