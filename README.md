# barter_site_dj

### Требования

Python 3.8 или выше
Django 4.x
SQLite (возможна модернизация для работы с PostgreSQL
virtualenv

### Установка
1) Введите в терминале: git clone https://github.com/lukashouknnootta22/barter_site_dj.git
2) Создайте и активируйте виртуальное окружение: python -m venv venv
     Для Windows: venv\Scripts\activate
     Для Linux: source venv/bin/activate
3) Установите зависимости: pip install -r requirements.txt
4) Создайте и примените миграции: python manage.py makemigrations & python manage.py migrate
5) Проведите тесты (опцианально): python manage.py test
6) Создайте суперпользователя для работы с админ-панелью: python manage.py createsuperuser
7) Запустите сервер: python manage.py runserver (DEBUG выключен, ALLOWED_HOSTS уже стоит локальный хост)

Теперь перейдя по адресу http://127.0.0.1:8000/ вы попадёте на главную страницу
