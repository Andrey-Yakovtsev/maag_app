
# PRODUCTION PART
buildup_prod:
	docker compose -f production.yml up --build

up_prod:
	docker compose -f production.yml up -d

superuser_prod:
	docker compose -f production.yml run --rm django python manage.py createsuperuser

down_prod:
	docker compose -f production.yml down

kill_prod:
	docker compose -f production.yml down -v

migrations_prod:
	docker compose -f production.yml run --rm django python manage.py makemigrations

migrate_prod:
	docker compose -f production.yml run --rm django python manage.py migrate

fill_db_prod:
	docker compose -f production.yml run --rm django python manage.py init_db_fulfilment

clean_db_prod:
	docker compose -f production.yml run --rm django python manage.py clean_db


# LOCAL PART
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

# Линуксовые версии

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
	docker stop maag_app_local_django
	docker compose -f local.yml run --rm django python manage.py makemigrations

migrate:
	docker stop maag_app_local_django
	docker compose -f local.yml run --rm django python manage.py migrate

migrationsl:
	sudo docker stop maag_app_local_django
	sudo docker-compose -f local.yml run --rm django python manage.py makemigrations

migratel:
	sudo docker stop maag_app_local_django
	sudo docker-compose -f local.yml run --rm django python manage.py migrate

fill_dbl:
	sudo docker stop maag_app_local_django
	sudo docker-compose -f local.yml run --rm django python manage.py init_db_fulfilment

heavy_dbl:
	sudo docker stop maag_app_local_django
	sudo docker-compose -f local.yml run --rm django python manage.py heavy_db_load
	sudo docker run maag_app_local_django

fill_db:
	docker stop maag_app_local_django
	docker compose -f local.yml run --rm django python manage.py init_db_fulfilment

clean_db:
	docker stop maag_app_local_django
	docker compose -f local.yml run --rm django python manage.py clean_db

clean_dbl:
	sudo docker stop maag_app_local_django
	sudo docker-compose -f local.yml run --rm django python manage.py clean_db
