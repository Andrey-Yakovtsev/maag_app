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
	docker-compose -f local.yml up --build

upl:
	docker-compose -f local.yml up

downl:
	docker-compose -f local.yml down

killl:
	docker-compose -f local.yml down -v

superuserl:
	docker-compose -f local.yml run --rm django python manage.py createsuperuser
