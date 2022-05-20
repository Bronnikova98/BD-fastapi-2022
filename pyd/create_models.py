from pydantic import BaseModel, Field
from datetime import date
from typing import List

# модели, которые используются при создании/редактировании сущностей

class ClimberCreate(BaseModel):
    surname: str = Field(..., max_length=255, example='Иванов')
    name: str = Field(..., max_length=255, example='Иван')    
    patronymic: str = Field(None, max_length=255, example='Иванович')
    address: str = Field(..., max_length=255, example='г. Москва, ул. Красногвардейская, 59')
   
    class Config:
        orm_mode = True
        
class ClimberCreate5(BaseModel):

    surname: str = Field(..., max_length=255, example='Иванов')
    name: str = Field(..., max_length=255, example='Иван')    
    patronymic: str = Field(None, max_length=255, example='Иванович')
    address: str = Field(..., max_length=255, example='г. Москва, ул. Красногвардейская, 59')
    climbing_ids: List[int] = None

    class Config:
        orm_mode = True

class ClimbingCreate(BaseModel):
    date_start: date = Field(..., example='2022-05-12')
    date_end: date = Field(None, example='2022-05-30')
    name_group: str = Field(..., max_length=255, example='Группа1')
    # связь 1 к n 
    mountain_id: int = Field(..., gt=0, example=1)

    climber_ids: List[int] = None

    class Config:
        orm_mode = True

class ClimbingCreate8(BaseModel):
    date_start: date = Field(..., example='2022-05-12')   
    name_group: str = Field(..., max_length=255, example='Группа1')
    # связь 1 к n 
    mountain_id: int = Field(..., gt=0, example=1)

    class Config:
        orm_mode = True
        
class MountainCreate(BaseModel):
    name: str = Field(..., max_length=255, example='Гора1')
    height: int = Field(None, gt=0, example=1000)
    country_district: str = Field(None, max_length=255, example='Город, район')

    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    username: str = Field(..., max_length=255, example='Логин')
    password: str = Field(..., max_length=255, example='Пароль')
    
    class Config:
        orm_mode = True