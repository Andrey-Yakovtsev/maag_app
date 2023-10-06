# maag-app

MAAG App

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


## Основные команды

Запилил все Основные команды на [Make-file](Makefile):

Если у тебя линукс - make-команда содержит постфикс - l.
Типа `buildup` - для мака и `buildupl` - для линукса.
Это потому что подман на линуксе стартует через старую версию docker-compose (через дефис)

Собрать и поднять проект `make buildup`

Поднять уже собраный проект `make up`

Опустить контейнеры `make down`

Опустить контейнеры, удалить все данные и прибинденные вольюмы
  `make kill`

Некоторые команды в текущей версии шаблона кукикаттер просят, чтобы основной контейнер с приложением гасился
для выполнения команд связанных с приложением. Типа миграции или шелл.
Для таких случаев в после выполнения команды надо сделать `make up`

**Пример для линукса:**

пошел в шелл, что-то поделал:
  `make shelll`
потом поднял основной конт на место:
``make upl``


### Как поднять проект.
После того, как затащил проект (на примере Линукс-версии):
1. `make buildupl`
2. `make superuserl` - обрати внимание - логин по и-мейлу
3. `make fill_db` - скрипт заполнения БД моками

Если по какой-то причине миграции не поднялись. Но должы сами при сборке.
1. `make migrations`
1. `make migrate` и снова
3. `make fill_db`


### PG-Admin

На http://localhost:5050/
Найдешь контейнер с PG-admin.
Креды вот:
      PGADMIN_DEFAULT_EMAIL: 123@email.com
      PGADMIN_DEFAULT_PASSWORD: admin
Вообще они лежат в файлике для локальной сборки [local.yaml](local.yml)


### Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy maag_app

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd maag_app
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd maag_app
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd maag_app
celery -A config.celery_app worker -B -l info
```

### Email Server

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server [MailHog](https://github.com/mailhog/MailHog) with a web interface is available as docker container.

Container mailhog will start automatically when you will run all docker containers.
Please check [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html) for more details how to start all containers.

With MailHog running, to view messages that are sent by your application, open your browser and go to `http://127.0.0.1:8025`

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).
