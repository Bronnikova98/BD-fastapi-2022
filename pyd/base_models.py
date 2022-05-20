from pydantic import BaseModel, Field
from datetime import date

# файл с базовыми моделями

class ClimberBase(BaseModel):
    id: int = Field(None, gt=0, example=1)
    surname: str = Field(..., max_length=255, example='Иванов')
    name: str = Field(..., max_length=255, example='Иван')    
    patronymic: str = Field(None, max_length=255, example='Иванович')
    address: str = Field(..., max_length=255, example='г. Москва, ул. Красногвардейская, 59')
    
    class Config:
        orm_mode=True      
    
class ClimbingBase(BaseModel):
    id: int = Field(None, gt=0, example=1)
    date_start: date = Field(..., example='2022-05-12')
    date_end: date = Field(None, example='2022-05-30')
    name_group: str = Field(..., max_length=255, example='Группа1')
    # связь 1 к n 
    mountain_id: int = Field(..., gt=0, example=1)
    
    class Config:
        orm_mode = True
        
class MountainBase(BaseModel):
    id: int = Field(None, gt=0, example=1)
    name: str = Field(..., max_length=255, example='Гора1')
    height: int = Field(None, gt=0, example=1000)
    country_district: str = Field(None, max_length=255, example='Город, район')
    
    class Config:
        orm_mode=True 
    
class BaseUser(BaseModel):
    id: int = Field(None, gt=0, example=1)
    username: str = Field(..., max_length=255, example='Логин')
       
    class Config:
        orm_mode = True