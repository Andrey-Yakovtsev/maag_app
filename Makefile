buildup:
	docker compose -f local.yml up --build

up:
	docker compose -f local.yml up -d

down:
	docker compose -f local.yml down

kill:
	docker compose -f local.yml down -v

migrate:
	docker compose -f local.yml run --rm django python manage.py migrate

superuser:
	docker compose -f local.yml run --rm django python manage.py createsuperuser
