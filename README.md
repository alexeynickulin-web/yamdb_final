### Статус workflow:
![example workflow](https://github.com/alexeynickulin-web/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

### Ссылка на развёрнутый проект:

http://158.160.10.201/admin/


### Цель проекта:

Проект YaMDb собирает отзывы пользователей на произведения.
Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
Список категорий может быть расширен администратором.


### Шаблон наполнения env-файла:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

### Как запустить проект:

- Клонируйте репозиторий и перейдите в него

```
git clone git@github.com:alexeynickulin-web/yamdb_final.git
```

```
cd infra
```

- Выполните сборку контейнеров

```
docker-compose up -d --build
```

- Выполните миграцию БД и сборку статики

```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

- Выполните команду по наполнению БД из файла фикстур

```
docker-compose exec web python manage.py loaddata fixtures.json
```

- Также можно выполнить резервную копию базы

```
docker-compose exec web python manage.py dumpdata > fixtures.json 
```

### Автор проекта: 

**[Алексей](https://github.com/alexeynickulin-web)**