from fastapi import FastAPI
import models
from database import engine
from routers import climber_router, climbing_router, mountain_router, user_router

# создание таблиц в БД из моделей
models.Base.metadata.create_all(bind=engine)

# инициализация фастапи
app = FastAPI()

# подключение АпиРоутера (маршруты сущности)
app.include_router(climber_router)
app.include_router(climbing_router)
app.include_router(mountain_router)
app.include_router(user_router)