buildup:
	docker compose -f local.yml up --build

up:
	docker compose -f local.yml up -d

down:
	docker compose -f local.yml down

kill:
	docker compose -f local.yml down -v

superuser:
	docker compose -f local.yml run --rm django python manage.py createsuperuser

buildupl:
	sudo docker-compose -f local.yml up --build

upl:
	sudo docker-compose -f local.yml up

downl:
	sudo docker-compose -f local.yml down

killl:
	sudo docker-compose -f local.yml down -v

superuserl:
	sudo docker stop maag_app_local_django
	sudo docker-compose -f local.yml run --rm django python manage.py createsuperuser

shelll:
	sudo docker stop maag_app_local_django
	sudo docker-compose -f local.yml run --rm django python manage.py shell_plus

migrations:
	sudo docker stop maag_app_local_django
	sudo docker-compose -f local.yml run --rm django python manage.py makemigrations

migrate:
	sudo docker stop maag_app_local_django
	sudo docker-compose -f local.yml run --rm django python manage.py migrate
