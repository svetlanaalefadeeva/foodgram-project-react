![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

## Foodgram  🍝

Foodgram - это веб-приложение, которое позволяет пользователям делиться рецептами своих любимых блюд. 
Оно предоставляет удобный интерфейс для загрузки, просмотра и добавления в избранное, подписку на авторов и создание списка покупок.


### Проект доступен по адресу:
[https://foodgramfox.hopto.org/](https://foodgramfox.hopto.org/)
- **email**: admin@admin.com
- **password**: 1234


## Технологии

- Python 3.9
- Django 3.2.3
- Django REST framework 3.12.4
- JavaScript

## Запуск проекта из образов с Docker hub

Для запуска необходимо на создать папку проекта, например `foodgram` и перейти в нее:

```bash
mkdir foodgram
cd foodgram
```

В папку проекта скачиваем файл `docker-compose.production.yml` и запускаем его:

```bash
sudo docker compose -f docker-compose.production.yml up
```

Произойдет скачивание образов, создание и включение контейнеров, создание томов и сети.

### Запуск проекта из исходников GitHub

Клонируем себе репозиторий: 

```bash 
git@github.com:svetlanaalefadeeva/foodgram-project-react.git
```

Выполняем запуск:

```bash
sudo docker compose -f docker-compose.yml up
```

### После запуска: Миграции, сбор статистики

После запуска необходимо выполнить сбор статистики и миграции бэкенда. Статистика фронтенда собирается во время запуска контейнера, после чего он останавливается. 

```bash
sudo docker compose -f [имя-файла-docker-compose.yml] exec backend python manage.py migrate

sudo docker compose -f [имя-файла-docker-compose.yml] exec backend python manage.py collectstatic

sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/static/. /backend_static/static/

sudo docker compose -f docker-compose.production.yml exec backend python manage.py created_db
```

И далее проект доступен на: 

```
http://localhost:8080/
```

### Остановка оркестра контейнеров

В окне, где был запуск **Ctrl+С** или в другом окне:

```bash
sudo docker compose -f docker-compose.yml down
```

### Автор проекта Foodgram 🍝

- Backend: [Светлана Фадеева](https://github.com/svetlanaalefadeeva)
- Frontend: Yandex Praktikum team
