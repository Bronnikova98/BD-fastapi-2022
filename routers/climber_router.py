from itertools import count, groupby
from statistics import mode
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import models
from database import get_db
import pyd
from datetime import date
from auth import AuthHandler

router = APIRouter(
    prefix="/climber",
    tags=["climber"]
)

# экземпляр чтобы защитить маршрут
auth_handler=AuthHandler()

# получение всех альпинистов
@router.get("/", response_model=List[pyd.ClimberSchema])
async def get_climbers(db: Session = Depends(get_db)):
    return db.query(models.Climber).all()

# получение альпиниста по id
@router.get("/{climber_id}")
async def get_climber_by_id(climber_id: int, db: Session = Depends(get_db)):
    q = db.query(models.Climber).filter(models.Climber.id == climber_id).first()
    if q:
        return q
    raise HTTPException(status_code=404, detail="Climber not found")

# добавление альпиниста
@router.post("/", response_model=pyd.ClimberSchema)
async def create_climber(climber_input: pyd.ClimberCreate, username=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    # автозаполнение  всех полей
    climber_db = models.Climber(
        **climber_input.dict()
    )
    db.add(climber_db)
    db.commit()
    return climber_db

# обновление альпиниста
@router.put("/{climber_id}", response_model=pyd.ClimberSchema)
async def climber_update(climber_input: pyd.ClimberCreate, climber_id: int, username=Depends(auth_handler.auth_wrapper), db:Session = Depends(get_db)):
    db_climber = db.query(models.Climber).filter(
        models.Climber.id == climber_id
    ).first()
    # проверка существования альпиниста
    if db_climber == None:
        raise HTTPException(status_code=404, detail="Climber not found")
    else:
        db_climber.surname=climber_input.surname
        db_climber.name=climber_input.name
        db_climber.patronymic=climber_input.patronymic
        db_climber.address=climber_input.address
        db.commit()
        return db_climber

# удаление альпиниста
@router.delete("/{climber_id}")
async def climber_delete(climber_id: int, username=Depends(auth_handler.auth_wrapper), db:Session = Depends(get_db)):
    db_climber = db.query(models.Climber).filter(
        models.Climber.id == climber_id
    ).first()
    if db_climber == None:
        raise HTTPException(status_code=404, detail="Climber not found")
    else:    
        db_climber = db.query(models.Climber).filter(
            models.Climber.id == climber_id
        ).delete()    
        db.commit()
        return 'deletion completed'
               
# 5) Предоставить возможность добавления нового альпиниста в состав указанной группы 
# нельзя добавить нового альпиниста в несуществующую группу/восхождение
@router.post("/5/", response_model=pyd.ClimberSchema)
async def climber_climbing_add(climber_input: pyd.ClimberCreate5, username=Depends(auth_handler.auth_wrapper), db:Session = Depends(get_db)):   
    
    db_climber = models.Climber()
    
    db_climber.surname=climber_input.surname
    db_climber.name=climber_input.name
    db_climber.patronymic=climber_input.patronymic   
    db_climber.address=climber_input.address    
   
    # пройтись по циклу с id восхождений, искать их в БД, если есть добавить, иначе ошибка
    for climbing_id in climber_input.climbing_ids:
       
        climber_db = db.query(models.Climbing).filter(models.Climbing.id == climbing_id).first()
       
        if climber_db:
            db_climber.climbings.append(climber_db)
        else:
            raise HTTPException(status_code=404, detail="Climbing not found")      
        
    db.add(db_climber)        
    db.commit()  
    return db_climber

# 4) Показать список альпинистов, осуществлявших восхождение в указанный интервал дат
@router.get("/4/{date_from}/{date_to}")
async def climber_climbing_date(date_from: date,  date_to: date, db:Session = Depends(get_db)):
    climb_db=db.query(models.Climber).join(models.Climbing.climbers).filter(
        models.Climbing.date_start >= date_from,
        models.Climbing.date_start <= date_to
    ).all()
    return climb_db

# 6) Показать информацию о количестве восхождений каждого альпиниста на каждую гору
@router.get("/6/")
async def climbing_counter(db:Session = Depends(get_db)): 
    
    db_climbing_count = db.query(models.Mountain, models.Climber, func.count('models.Climbing.id').label('climbing_count')).join(
            models.Climbing.climbers
        ).filter(
            models.Climbing.mountain_id == models.Mountain.id
        ).group_by(models.Mountain, models.Climber).all()            
        
    return db_climbing_count

# работает некорректно, нужно исправить
# 9) Предоставить информацию о том, сколько альпинистов побывали на каждой горе
@router.get("/9/")
async def climber_counter(db:Session = Depends(get_db)):    
   
    db_climber_count = db.query(models.Mountain, func.count('models.Climber.id').label('climber_count')).join(
            models.Climbing.mountains, models.Climbing.climbers
        ).filter(
            models.Climbing.mountain_id == models.Mountain.id            
        ).group_by(models.Mountain).all()
        
    return db_climber_count