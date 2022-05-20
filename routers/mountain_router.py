from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
from database import get_db
import pyd
from auth import AuthHandler

router = APIRouter(
    prefix="/mountain",
    tags=["mountain"]
)

# экземпляр чтобы защитить маршрут
auth_handler=AuthHandler()

# получение всех гор
@router.get("/", response_model=List[pyd.MountainBase])
async def get_moutnains(db: Session = Depends(get_db)):
    return db.query(models.Mountain).all()

# получение горы по id
@router.get("/{mountain_id}")
async def get_mountain_by_id(mountain_id: int, username=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    q = db.query(models.Mountain).filter(models.Mountain.id == mountain_id).first()
    if q:
        return q
    raise HTTPException(status_code=404, detail="Mountain not found")

# добавление горы
# 2) Предоставить возможность добавления новой вершины, с указанием названия вершины, высоты и страны местоположения
@router.post("/", response_model=pyd.MountainBase)
async def create_moutnain(mountain_input: pyd.MountainCreate, username=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    
    # проверяем уникальность имени горы, если такое имя существует, то ошибка, иначе добавляем гору
    mont_db = db.query(models.Mountain).filter(models.Mountain.name == mountain_input.name).first()
    if mont_db:
        raise HTTPException(status_code=400, detail="This mountain name already exists")
    else:
        # автозаполнение  всех полей
        moutnain_db = models.Mountain(
        **mountain_input.dict()
        )            
        db.add(moutnain_db)
        db.commit()
        return moutnain_db
    
# обновление горы
@router.put("/{mountain_id}", response_model=pyd.MountainBase)
async def mountain_update(mountain_input: pyd.MountainCreate, mountain_id: int, username=Depends(auth_handler.auth_wrapper), db:Session = Depends(get_db)):
    db_mountain = db.query(models.Mountain).filter(
        models.Mountain.id == mountain_id
    ).first()
    
    if db_mountain == None:
        raise HTTPException(status_code=404, detail="Mountain not found")
    else:
        # проверяем уникальность имени горы, если такое имя существует, то ошибка, иначе обновляем гору
        mont_db = db.query(models.Mountain).filter(models.Mountain.name == mountain_input.name).first()    
        if db_mountain.name == mountain_input.name or mont_db == None:            
                db_mountain.name=mountain_input.name
                db_mountain.height=mountain_input.height
                db_mountain.country_district=mountain_input.country_district
                db.commit()
                return db_mountain
        elif db_mountain.name != mountain_input.name:
            raise HTTPException(status_code=400, detail="This mountain name already exists")

# удаление горы
@router.delete("/{mountain_id}")
async def mountain_delete(mountain_id: int, username=Depends(auth_handler.auth_wrapper), db:Session = Depends(get_db)):
    db_mountain = db.query(models.Mountain).filter(
        models.Mountain.id == mountain_id
    ).first()
    if db_mountain == None:
        raise HTTPException(status_code=404, detail="Mountain not found")
    else: 
        db_mountain = db.query(models.Mountain).filter(
            models.Mountain.id == mountain_id
        ).delete()    
        db.commit()
        return 'deletion completed'
    
# 1) Для каждой горы показать список групп, осуществлявших восхождение, в хронологическом порядке
@router.get("/1/group_climbing")
async def group_climbing(db:Session = Depends(get_db)):    
    db_group = db.query(models.Mountain.name, models.Climbing.name_group, models.Climbing.date_start).filter(models.Mountain.id == models.Climbing.mountain_id).all()
    sorted_group= sorted(db_group, key=lambda d: d['date_start'])    
    return sorted_group

# 3) Предоставить возможность изменения данных о вершине, если на нее не было восхождений
@router.put("/3/{id_mountain}", response_model=pyd.MountainBase)
async def mountain_update_not_climbing(mountain_input: pyd.MountainCreate, id_mountain: int, username=Depends(auth_handler.auth_wrapper), db:Session = Depends(get_db)):
    db_mountain = db.query(models.Mountain).filter(
        models.Mountain.id == id_mountain
    ).first()    
    if db_mountain == None:
        raise HTTPException(status_code=404, detail="Mountain not found")
    else: 
        db_climbing=db.query(models.Climbing).filter(
        models.Climbing.mountain_id == id_mountain
        ).first()
        print(db_climbing)
        if db_climbing == None:
            # проверяем уникальность имени горы, если такое имя существует, то ошибка, иначе обновляем гору
            mont_db = db.query(models.Mountain).filter(models.Mountain.name == mountain_input.name).first()    
            if db_mountain.name == mountain_input.name or mont_db == None:
                
                db_mountain.name=mountain_input.name
                db_mountain.height=mountain_input.height
                db_mountain.country_district=mountain_input.country_district        
                db.commit()
            
                return db_mountain
            elif db_mountain.name != mountain_input.name:
                raise HTTPException(status_code=400, detail="This mountain name already exists")
        else:        
            return db_climbing