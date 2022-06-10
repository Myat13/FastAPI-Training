# standard lib import
from datetime import datetime, timedelta

# FastApi import 
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

# Sqlalchemy import
from sqlalchemy.orm import Session

# jose lib import 
from jose import JWTError, jwt

# Dir import 
from . import schema, database, models
from .config import settings



# Some magic OAUTH2 did i don't understand
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Update the data argument
    to_encode.update({'exp': expire})
    
    # Encoding data with jwt module form jose libary
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY)
    
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    
    try:
        payload =  jwt.decode(token, SECRET_KEY)
    
        id: str = payload.get('user_id')
    
        if id is None:
            raise credentials_exception
        token_data = schema.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data
    

def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
        )
    
    token = verify_access_token(token, credentials_exception)
    
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user