from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import init_db, close_db
from app.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    close_db()

app = FastAPI(
    title="Python Glossary API",
    description="API для управления глоссарием терминов Python",
    version="1.0.0",
    lifespan=lifespan
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение маршрутов
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Python Glossary API", "docs": "/docs"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/readyz")
async def readiness_probe():
    return {"status": "ready"}