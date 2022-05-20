from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
from database import get_db
import pyd
from auth import AuthHandler

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

# экземляр
auth_handler=AuthHandler()

@router.post("/register", response_model=pyd.BaseUser)
async def register_user(user_input: pyd.CreateUser, db: Session = Depends(get_db)):
    
    user_db=db.query(models.User).filter(
        models.User.username == user_input.username
    ).first()
    
    if user_db:
        raise HTTPException(400, 'Такой есть')
    hash_pass=auth_handler.get_passwird_hash(user_input.password)
    
    user_db=models.User(
        username=user_input.username,
        password=hash_pass
    )
    db.add(user_db)
    db.commit()    
    return user_db

@router.post("/login")
async def user_login(user_input: pyd.CreateUser, db: Session = Depends(get_db)):
    user_db=db.query(models.User).filter(
        models.User.username == user_input.username
    ).first()
    if not user_db:
        raise HTTPException(404, 'Пользователя с таким логином нет')
    
    if auth_handler.verify_password(user_input.password, user_db.password):
        token = auth_handler.encode_token(user_db.username)
        return {'token': token}
    else:
         raise HTTPException(403, 'Пароль не верный')