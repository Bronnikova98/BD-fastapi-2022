from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
from database import get_db
import pyd
from datetime import date
from auth import AuthHandler

router = APIRouter(
    prefix="/climbing",
    tags=["climbing"]
)

# экземпляр чтобы защитить маршрут
auth_handler=AuthHandler()

# получение всех восхождений
@router.get("/", response_model=List[pyd.ClimbingSchema])
async def get_climbings(db: Session = Depends(get_db)):
    return db.query(models.Climbing).all()

# получение восхождения по id
@router.get("/{climbing_id}")
async def get_climbing_by_id(climbing_id: int, db: Session = Depends(get_db)):
    q = db.query(models.Climbing).filter(models.Climbing.id == climbing_id).first()
    if q:
        return q
    raise HTTPException(status_code=404, detail="Climbing not found")


# добавление восхождения
# нельзя добавить существующее имя группы
# нельзя добавить восхождение на несуществующую гору
@router.post("/", response_model=pyd.ClimbingSchema)
async def create_climbing(climbing_input: pyd.ClimbingCreate, username=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
       
    # проверяем уникальность имени группы, если такое имя существует, то ошибка
    climbi_db = db.query(models.Climbing).filter(models.Climbing.name_group == climbing_input.name_group).first()
    if climbi_db:
        raise HTTPException(status_code=400, detail="This group name already exists")
    else:
        # проверяем что гора существует
        mount_db = db.query(models.Mountain).filter(models.Mountain.id == climbing_input.mountain_id).first()
        if mount_db == None:
            raise HTTPException(status_code=404, detail="Mountain not found")           
        else:            
             # создание восхождения
            climbing_db = models.Climbing()            
                        
            # пройтись по циклу с id альпинистов, искать их в БД, если есть добавить, иначе ошибка
            for climber_id in climbing_input.climber_ids:
                climber_db = db.query(models.Climber).filter(models.Climber.id == climber_id).first()
                if climber_db:
                    climbing_db.climbers.append(climber_db)
                else:
                    raise HTTPException(status_code=404, detail="Climber not found")
                
            climbing_db.date_start = climbing_input.date_start
            climbing_db.date_end = climbing_input.date_end
            climbing_db.name_group = climbing_input.name_group
            climbing_db.mountain_id = climbing_input.mountain_id
            
            db.add(climbing_db)
            db.commit()
            return climbing_db

# обновление восхождения
# нельзя обновить на существующее имя группы
# нельзя обновить восхождение на несуществующую гору
@router.put("/{climbing_id}", response_model=pyd.ClimbingSchema)
async def climbing_update(climbing_input: pyd.ClimbingCreate, climbing_id: int, username=Depends(auth_handler.auth_wrapper), db:Session = Depends(get_db)):
    db_climbing = db.query(models.Climbing).filter(
        models.Climbing.id == climbing_id
    ).first()
    
    # проверяем существование восхождения
    if db_climbing == None:
        raise HTTPException(status_code=404, detail="Climbing not found")
    else:
        # проверяем уникальность имени группы
        climbi_db = db.query(models.Climbing).filter(models.Climbing.name_group == climbing_input.name_group).first()
               
        if db_climbing.name_group == climbing_input.name_group or climbi_db == None:
            
            # проверяем что гора существует
            mount_db = db.query(models.Mountain).filter(models.Mountain.id == climbing_input.mountain_id).first()
            if mount_db == None:   
                raise HTTPException(status_code=404, detail="Mountain not found")                
            else:                
                db_climbing.date_start=climbing_input.date_start
                db_climbing.date_end=climbing_input.date_end
                db_climbing.name_group=climbing_input.name_group
                db_climbing.mountain_id=climbing_input.mountain_id
                db_climbing.climbers.clear()
                    
                # пройтись по циклу с id альпинистов, искать их в БД, если есть добавить, иначе ошибка
                for climber_id in climbing_input.climber_ids:
                    climber_db = db.query(models.Climber).filter(models.Climber.id == climber_id).first()                    
                    if climber_db:                        
                        db_climbing.climbers.append(climber_db)
                    else:
                        raise HTTPException(status_code=404, detail="Climber not found")                
                    
                db.commit()
                return db_climbing
        elif db_climbing.name_group != climbing_input.name_group:
            raise HTTPException(status_code=400, detail="This group name already exists")
                
# удаление восхождения
@router.delete("/{climb_id}")
async def climbing_delete(climb_id: int, username=Depends(auth_handler.auth_wrapper), db:Session = Depends(get_db)):
    db_climbing = db.query(models.Climber).filter(
        models.Climbing.id == climb_id
    ).first()
    if db_climbing == None:
        raise HTTPException(status_code=404, detail="Climbing not found")
    else: 
        db_climbing = db.query(models.Climbing).filter(
            models.Climbing.id == climb_id
        ).delete()
        # удаление связи при удалении восхождения
        db_climbing_conn = db.query(models.climber_climbing).filter(
            models.climber_climbing.columns.climbing_id == climb_id
        ).delete()       
        db.commit()
        return 'deletion completed'       
            
# 7) Показать список восхождений (групп), которые осуществлялись в указанный пользователем период времени
@router.get("/7/{date_from}/{date_to}")
async def climbing_date(date_from: date,  date_to: date, db:Session = Depends(get_db)):
    climb_db=db.query(models.Climbing).filter(
        models.Climbing.date_start >= date_from,
        models.Climbing.date_start <= date_to
    ).all()
    return climb_db

# 8) Предоставить возможность добавления новой группы, указав её название, вершину, дату начала восхождения
# нельзя добавить существующее имя группы
# нельзя добавить восхождение на несуществующую гору
@router.post("/8/", response_model=pyd.ClimbingSchema)
async def create_climbing(climbing_input: pyd.ClimbingCreate8, username=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
       
    # проверяем уникальность имени группы, если такое имя существует, то ошибка
    climbi_db = db.query(models.Climbing).filter(models.Climbing.name_group == climbing_input.name_group).first()
    if climbi_db:
        raise HTTPException(status_code=400, detail="This group name already exists")
    else:
        # проверяем что гора существует
        mount_db = db.query(models.Mountain).filter(models.Mountain.id == climbing_input.mountain_id).first()
        if mount_db == None:
            raise HTTPException(status_code=404, detail="Mountain not found")           
        else:            
             # создание восхождения
            climbing_db = models.Climbing()                                 
                
            climbing_db.date_start = climbing_input.date_start
            climbing_db.name_group = climbing_input.name_group
            climbing_db.mountain_id = climbing_input.mountain_id
            
            db.add(climbing_db)
            db.commit()
            return climbing_db