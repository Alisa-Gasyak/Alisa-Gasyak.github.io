# Python Glossary API

REST API для управления глоссарием терминов Python с использованием FastAPI и Docker.

## Совершаемые Операции

- Получение списка всех терминов
- Получение информации о конкретном термине по ключевому слову
- Добавление нового термина с описанием
- Обновление существующего термина
- Удаление термина из глоссария

## Создание

1. Клонировать репозиторий:
git clone <repository-url>
cd python-glossary-api

2. Установить зависимости:
pip install -r requirements.txt

3. Запустить сервер:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

## Запуск с Docker

1. Сборка и запуск
docker-compose up --build

2. Только сборка
docker build -t python-glossary-api 

3. Запуск контейнера
docker run -p 8000:8000 python-glossary-api

## Шаги развёртывания

1. Клонировать репозиторий

2. Собрать образ
docker-compose build

3. Запустить контейнер
docker-compose up -d

4. Проверить работу
curl http://localhost:8000/health
Собрать образ:
