
# fastapi import
from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

# sqlAlchemy import
from sqlalchemy.orm import Session

# base dir import
from .. import models, utils, schema, oauth2
from ..database import engine, get_db



router = APIRouter(tags=['Authentication']) # defining routes

@router.post('/login', response_model=schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')
        
    # Create token with oauth2 file jose lib
    access_token  = oauth2.create_access_token(data = {'user_id': user.id})
    
    #return
    return {'access_token': access_token, 'token_type': 'bearer'}
        











