# HW_24.1_drf

## Описание

Проект для онлайн-обучения, включающий курсы, уроки и подписки на курсы.

## Требования

- Docker
- Docker Compose


## Установка и запуск

Следуйте этим шагам, чтобы настроить и запустить проект.

### 1. Клонирование репозитория

Клонируйте репозиторий на ваш локальный компьютер:

```sh
git clone https://github.com/Crazilina/hw_24.1_drf.git
cd hw_24.1_drf
```

### 2. Создание сети Docker (если не существует)
Создайте сеть Docker, если она еще не создана:

```sh
docker network create hw_24_27_drf
```

### 3. Настройка переменных окружения
Скопируйте шаблон файла .env.sample в файл .env и отредактируйте его, добавив свои данные:
```sh
cp .env.sample .env
```

### 4. Запуск Docker Compose
Убедитесь, что у вас есть файл docker-compose.yml в корневой директории проекта. Запустите Docker Compose с пересборкой образов:
```sh
docker-compose up -d --build
```

### 5. Применение миграций и создание суперпользователя
Примените миграции базы данных и создайте суперпользователя для доступа к административной панели Django:
```sh
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## Полезные команды

- Остановка всех контейнеров:
```sh
docker-compose stop
```

- Удаление всех контейнеров:
```sh
docker-compose down
```

- Удаление всех томов:
```sh
docker volume prune -f
```