# pylib import 
from typing import Optional, List

# fastapi import
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

# sqlAlchemy import
from sqlalchemy.orm import Session

# base dir import
from .. import models, utils, schema
from ..database import get_db


router = APIRouter(
    prefix = '/users',
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    
    # hash password
    hash_password = utils.hash(user.password)
    user.password = hash_password
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
    
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schema.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {id} does not exists in database')
    
    return user


