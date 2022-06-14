# pylib import 
from typing import List, Optional

# fastapi import
from fastapi import status, HTTPException, Depends, APIRouter

# sqlAlchemy import
from sqlalchemy.orm import Session
from sqlalchemy import func

# base dir import
from .. import models, schema, oauth2
from ..database import get_db


# defining routes
router = APIRouter(
    prefix = '/posts',
    tags=['Posts']
)

# 

@router.get("/", response_model=List[schema.PostOut])
def get_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
             search: Optional[str] = '',Limit: int = 10, skip: int = 0):
    # cursor.execute(""" SELECT * FROM posts """)
    # my_posts = cursor.fetchall()
    # my_posts = db.query(models.Post).filter(models.Post.content.contains(search)).limit(Limit).offset(skip).all()
    
    results = db.query(
        models.Post, func.count(models.Vote.post_id).label('votes')).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
                models.Post.content.contains(search)).limit(Limit).offset(skip).all()

    return results


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute(
    #     """ INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published) 
    #     )
    
    # new_post = cursor.fetchone()
    
    # conn.commit()
    
    # Create new instance to the model object with post dict data
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    # Adding to the db
    db.add(new_post)
    # Save within db
    db.commit()
    # Refresh to display return json object
    db.refresh(new_post)
    
    return new_post


@router.get('/latest', response_model=schema.Post)
def get_latest_post(input: str,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = my_post[len(my_post) - 1]
    post = db.query(models.Post).filter(models.Post.title == input).first()
    if not post:
        print('no post')
    return post


@router.get('/{id}', response_model=schema.PostOut)
def get_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(
        models.Post, func.count(models.Vote.post_id).label('votes')).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
        
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} is not exists in database...")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'error': f"post with id: {id} is not exists in database..."}
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    # del_post = cursor.fetchone()      
    # conn.commit()
    
    del_post = db.query(models.Post).filter(models.Post.id == id)
    
    del_post_one = del_post.first()
    
    if del_post_one == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post does not exists...')
    
    post_owner_id = del_post_one.owner_id
    
    if post_owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not authorized to delet this post')
    
    
    del_post.delete(synchronize_session=False)
    db.commit()
    
    return {'message': 'post was successfully deleted'}
    

@router.put("/{id}", response_model=schema.Post)
def update_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""", (
    #     post.title, post.content, post.published, str(id)
    #     ))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to edit this post')
    
    post_query.update(post.dict(), synchronize_session=False )
    db.commit()
    
    return post_query.first()

