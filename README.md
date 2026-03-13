# Habit Tracker API

Бэкенд-сервис для отслеживания привычек с отправкой напоминаний через Telegram.

**Адрес сервера:** http://158.160.218.82

---

## Функциональность

- Регистрация и авторизация пользователей (JWT)
- CRUD операции с привычками
- Просмотр публичных привычек
- Пагинация (5 привычек на страницу)
- Валидация правил привычек
- Документация API (Swagger)
- Интеграция с Telegram
- Фоновые задачи через Celery + Redis
- Настроенный CORS

---

## Технологии

- Python 3.12
- Django 5.2 + Django REST Framework
- PostgreSQL 16
- Redis 7
- Celery + Celery Beat
- Nginx
- Docker + Docker Compose
- GitHub Actions (CI/CD)

---

## Запуск проекта локально через Docker

### 1. Клонировать репозиторий

```bash
git clone https://github.com/Ekaterina649/kurs_work_habit_tracker.git
cd kurs_work_habit_tracker
```

### 2. Создать файл .env

```bash
cp .env.example .env
```

Заполните `.env`:

```env
SECRET_KEY=ваш-секретный-ключ
DEBUG=False
ALLOWED_HOSTS=localhost 127.0.0.1

POSTGRES_DB=habit_tracker
POSTGRES_USER=postgres
POSTGRES_PASSWORD=ваш-пароль
HOST=db
PORT=5432

REDIS_URL=redis://redis:6379/0

TELEGRAM_ACCESS_TOKEN=ваш-токен-бота
```

### 3. Запустить проект одной командой

```bash
docker compose up -d --build
```

Приложение будет доступно по адресу: **http://localhost**

---

## Настройка CI/CD (GitHub Actions)

### Как работает пайплайн

При каждом `push` или `pull_request` в ветку `develop`:

1. **test** — запускает `flake8` и `python manage.py test`
2. **build** — проверяет сборку Docker-образа
3. **deploy** — деплоит на сервер (только при push в `develop`)

### Необходимые GitHub Secrets

Перейдите в `Settings - Secrets and variables - Actions` и добавьте:

 Секрет       Описание                                        

 `SECRET_KEY`  Django SECRET_KEY                               
 `SERVER_IP`   IP-адрес сервера                                
 `SSH_USER`    Пользователь SSH (ubuntu)                       
 `SSH_KEY`     Приватный SSH-ключ для подключения к серверу    
 `DEPLOY_DIR`  Путь на сервере (/var/www/habit_tracker)        

---

## Настройка удалённого сервера

### 1. Установка Docker

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo usermod -aG docker $USER
newgrp docker
```

### 2. Подготовка директории

```bash
sudo mkdir -p /var/www/habit_tracker
sudo chown $USER:$USER /var/www/habit_tracker
cd /var/www/habit_tracker
git clone https://github.com/Ekaterina649/kurs_work_habit_tracker.git .
git checkout docker-homework
```

### 3. Создать .env на сервере

```bash
nano .env
```

### 4. Создать SSH-ключ для деплоя

```bash
ssh-keygen -t ed25519 -C "github-actions" -f ~/.ssh/deploy_key
cat ~/.ssh/deploy_key.pub >> ~/.ssh/authorized_keys
cat ~/.ssh/deploy_key  # скопировать в GitHub Secret SSH_KEY
```

### 5. Запустить проект

```bash
docker compose up -d --build
```

---

## Валидаторы привычек

- Нельзя одновременно указывать вознаграждение и связанную привычку
- Время выполнения не более 120 секунд
- Связанной может быть только приятная привычка
- Приятная привычка не может иметь вознаграждение и связанную привычку
- Нельзя выполнять привычку реже 1 раза в 7 дней