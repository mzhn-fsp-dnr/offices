# Сервис отделений

## Стек

`Python`, `sqlalchemy`, `Pydantic`, `alembic`, `fastapi`

## Описание сервиса

Сервис позволяет управлять почтовыми отделениями. Здесь происходит основная логика связывания услуг и окон к отделениям

## Структура проекта

```
offices/
├── Dockerfile
├── Readme.md
├── .example.env            # Пример конфигурации для .env
├── alembic/                # Настройка миграций
├── alembic.ini
├── app/                    # Директория с проектом
│   ├── api/                # Директория с HTTP эндпоинтами
│   ├── core/               # Директория с конфигом
│   ├── db/                 # Директория с конфигурацией подключения БД
│   ├── models/             # Директория с моделями БД
│   ├── schemas/            # Схемы Pydantic
│   ├── services/           # Слой сервисов
│   └── main.py             # Точка входа
├── docker-compose.yml
└── requirements.txt        # python-пакеты
```

## Развертывание проекта

1. Склонируйте репозиторий

```bash
git clone https://github.com/mzhn-fsp-dnr/offices.git
```

2. Настройте приложение путем редактирования `.env` файла. Пример расположен в `.example.env`

3. Запустите приложение в Docker

```bash
docker compose up --build
```
