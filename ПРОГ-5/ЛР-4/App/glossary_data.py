initial_glossary = [
    {
        "term": "Python",
        "definition": "Интерпретируемый, высокоуровневый язык программирования общего назначения с динамической типизацией.",
        "category": "язык программирования",
        "examples": "print('Hello, World!')",
        "related_terms": ["интерпретатор", "динамическая типизация"]
    },
    {
        "term": "FastAPI",
        "definition": "Современный, быстрый веб-фреймворк для построения API на Python 3.6+.",
        "category": "веб-фреймворк",
        "examples": "from fastapi import FastAPI\napp = FastAPI()",
        "related_terms": ["API", "ASGI", "Pydantic"]
    },
    {
        "term": "Pydantic",
        "definition": "Библиотека для валидации данных и управления настройками с помощью аннотаций типов.",
        "category": "библиотека",
        "examples": "class User(BaseModel):\n    name: str\n    age: int",
        "related_terms": ["валидация", "типизация", "FastAPI"]
    },
    {
        "term": "Docker",
        "definition": "Платформа для разработки, доставки и запуска приложений в контейнерах.",
        "category": "контейнеризация",
        "examples": "docker build -t myapp .\ndocker run -p 8000:8000 myapp",
        "related_terms": ["контейнер", "Dockerfile", "docker-compose"]
    },
    {
        "term": "API",
        "definition": "Application Programming Interface — интерфейс программирования приложений.",
        "category": "архитектура",
        "examples": "REST API, GraphQL, SOAP",
        "related_terms": ["REST", "endpoint", "JSON"]
    },
    {
        "term": "CRUD",
        "definition": "Create, Read, Update, Delete — базовые операции для работы с данными.",
        "category": "паттерн",
        "examples": "Создание, чтение, обновление и удаление записей в БД",
        "related_terms": ["REST", "база данных"]
    },
    {
        "term": "async/await",
        "definition": "Синтаксис для работы с асинхронным кодом в Python.",
        "category": "асинхронность",
        "examples": "async def get_data():\n    data = await fetch_from_api()",
        "related_terms": ["asyncio", "корутина"]
    },
    {
        "term": "Dockerfile",
        "definition": "Текстовый файл с инструкциями для сборки Docker-образа.",
        "category": "контейнеризация",
        "examples": "FROM python:3.9\nCOPY . /app\nRUN pip install -r requirements.txt",
        "related_terms": ["Docker", "контейнер", "образ"]
    }
]