# rast88

# Руководство по развертыванию приложения с использованием Nginx, Gunicorn и базы данных PostgreSQL

## Шаг 1: Установка необходимых зависимостей

Убедитесь, что у вас установлены `gunicorn`, `nginx` и PostgreSQL. Если они еще не установлены, вы можете установить их с помощью следующих команд:

```bash
pip install gunicorn
sudo apt-get install nginx
sudo apt-get install postgresql postgresql-contrib
```

## Шаг 2: Клонирование репозитория

Сначала склонируйте свой репозиторий с помощью команды:
```bash
git clone https://github.com/ваш-путь-к-репозиторию.git
cd ваш-путь-к-репозиторию
```

## Шаг 3: Установка зависимостей из requirements.txt

Установите зависимости из файла requirements.txt, чтобы удостовериться, что все необходимые пакеты установлены:
```bash
pip install -r requirements.txt
```

## Шаг 4: Настройка базы данных PostgreSQL

В файле приложения app.py изменить значения словаря db_params
```python
db_params = {
    'dbname': 'mydatabase',
    'user': 'myuser',
    'password': 'mypassword',
    'host': 'localhost',
    'port': '5432'
}
```


## Шаг 5: Настройка Gunicorn

Создайте сервисный файл для Gunicorn:
```bash
sudo nano /etc/systemd/system/myapp.service
```
Вставьте следующий код, заменив <путь_к_папке_проекта> на реальный путь к папке, в которой находится app.py:
```ini
[Unit]
Description=Gunicorn instance to serve myapp
After=network.target

[Service]
User=ваше_имя_пользователя
Group=ваша_группа
WorkingDirectory=/путь/к/папке/проекта
ExecStart=/usr/local/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target
```
Сохраните и закройте файл.

## Шаг 6: Настройка Nginx

Создайте конфигурационный файл для Nginx:
```bash
sudo nano /etc/nginx/sites-available/myapp
```

Вставьте следующий конфиг, заменив example.com на ваш домен или IP-адрес:
```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }

    location /static {
        alias /путь/к/папке/проекта/static;
    }

    location /favicon.ico {
        alias /путь/к/папке/проекта/favicon.ico;
    }
}
```
Создайте символическую ссылку на этот файл в директории sites-enabled:
```bash
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled
```

Перезапустите Nginx:
```bash
sudo systemctl restart nginx
```
## Шаг 7: Запуск Gunicorn и проверка

Запустите Gunicorn через systemd:
```bash
sudo systemctl start myapp
```
Проверьте состояние сервиса:
```bash
sudo systemctl status myapp
```







