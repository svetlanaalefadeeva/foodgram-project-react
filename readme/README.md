# Foodgram

Foodgram - это веб-приложение, которое позволяет пользователям делиться рецептами своих любимых блюд. 
Оно предоставляет удобный интерфейс для загрузки, просмотра и добавления в избранное, подписку на авторов и создание списка покупок.


### Проект доступен по адресу:
[https://foodgramfox.hopto.org/](https://foodgramfox.hopto.org/)
- **email**: admin@admin.com
- **password**: 1234


## Технологии

- Python 3.9
- Django 4.2.3
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
cd infra
git@github.com:svetlanaalefadeeva/foodgram-project-react.git
```

Выполняем запуск:

```bash
sudo docker compose -f docker-compose.yml up
```

### После запуска: миграции, сбор статистики, загрузка ингредиентов

После запуска необходимо выполнить сбор статистики и миграции бэкенда. Статистика фронтенда собирается во время запуска контейнера, после чего он останавливается. 

```bash
sudo docker compose -f [имя-файла-docker-compose.yml] exec backend python manage.py migrate

sudo docker compose -f [имя-файла-docker-compose.yml] exec backend python manage.py collectstatic

sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/static/. /backend_static/static/

sudo docker compose -f docker-compose.production.yml exec backend python manage.py created_db
```
Создайте суперпользователя
```bash
sudo docker compose -f [имя-файла-docker-compose.yml] exec backend python manage.py createsuperuser
```
И далее проект доступен на: 

```
http://localhost:8080/
```
Зайдите в админку
```bash
http://localhost:8080/admin
создайте теги для рецептов
```
И можете пользоваться сайтом. 
### Остановка оркестра контейнеров

В окне, где был запуск **Ctrl+С** или в другом окне:

```bash
sudo docker compose -f docker-compose.yml down
```

### Автор проекта Foodgram

- Backend: [Светлана Фадеева](https://github.com/svetlanaalefadeeva)
- Frontend: Yandex Praktikum team
