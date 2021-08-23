# API for surveys
## Вниманию представляется API для системы опросов пользователей


#### Функционал для администратора системы:
- авторизация в системе (регистрация не нужна)
- добавление/изменение/удаление опросов. Атрибуты опроса: название, дата старта, дата окончания, описание. После создания поле "дата старта" у опроса менять нельзя
- добавление/изменение/удаление вопросов в опросе. Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)

#### Функционал для пользователей системы:
- получение списка активных опросов
- прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов
- получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя


## Окружение проекта:
  * python 3.8
  * Django 2.2.10
  * djangorestframework


# Выполнить следующие команды:

## Инструкции

Для запуска проекта необходимо:
1. Создать базу данных PostgreSQL:
   ```` sql
    CREATE USER basic with password basic1;
    CREATE DATABASE basic_db WITH OWNER basic;
    ALTER USER basic CREATEDB;
   
2. Установить зависимости:
   ````
    pip install -r requirements.txt
   
3. Произвести миграции:
   ````
   python manage.py migrate
   
4. Загрузить тестовые данные:
   ````
   python manage.py loaddata fixtures.json

5. Для запуска сервера выполнить команду:
    ````
    python manage.py runserver

6. Примеры запросов представлены в файле requests.http
