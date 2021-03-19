API для сервиса music-events-project 

# Description
Проект music-events-project позволяет авторизованным пользователям создавать
музыкальные события, искать трэки по названию и автору в lastfm, добавлять 
понравившиеся трэки к определенному музыкальному мероприятию и голосовать
за понравившиеся трэки.


## Алгоритм регистрации пользователей
Пользователь отправляет POST-запрос с параметром username и password на адрес
`/registration/`. После регистрации необходимо получить токен авторизации по адресу
`/token/` и сменить его `token/refresh/`, если токен скомпрометирован.


# Getting Started
Создайте .env в корне проекта с настройками для подключения к БД.
```
- DB_ENGINE=django.db.backends.postgresql
- DB_NAME=Имя БД
- POSTGRES_USER=пользователь
- POSTGRES_PASSWORD=пароль
- DB_HOST=db
- DB_PORT=5432
```

Запуск проекта выполняется командой `docker-compose up`
 
Далее необходимо выполнить следующий шаги:
 - открываем терминал `docker exec -it web bash`
 - создание миграций `python manage.py makemigrations`
 - миграция `python manage.py migrate`
 - собираем статические файлы `python manage.py collectstatic`
 - создание администратора `python manage.py createsuperuser`
 
 
# Built With
- DRF - Django Rest Framework
- PostgreSQL
- Nginx 
- Docker
- Docker-compose


# Versioning
На данный момент версия проекта v1. Чтобы узнать доступные версии смотрите теги в этом репозитории.

# Endpoints
Документацию по конечным точкам АПИ смотрите по адресу `/redoc/`

# Authors
Balashov Konstantin

# Acknowledgments
Спасибо, всем кто воспользовался данным сервисом, буду рад обратной связи.
