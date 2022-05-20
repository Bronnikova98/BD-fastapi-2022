# в этом файле подключаются все маршрутизаторы апи, у каждого меняется название
from .climber_router import router as climber_router
from .climbing_router import router as climbing_router
from .mountain_router import router as mountain_router
from .user_router import router as user_router