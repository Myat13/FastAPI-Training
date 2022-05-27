my_post = [
    {'title': 'post 1', 'content': 'post 1 content', 'id': 1},
    {'title': 'post 2', 'content': 'post 1 content', 'id': 2},
]

def find_post(id):
    for post in my_post:
        if post['id'] == id:
            return post
        
def find_post_index(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i
        
        
        
# # This is comment create
# @router.post('/comments', status_code=status.HTTP_201_CREATED, response_model=schema.Comment)
# def create_comment(comment: schema.Comment, db: Session = Depends(get_db)):
    
#     # cursor.execute( """ INSERT INTO comments (content) VALUES (%s) RETURNING * """, (comment.content,))
    
#     # comment = cursor.fetchone()
    
#     # conn.commit()
    
#     comment = models.Comment(**comment.dict())
#     db.add(comment)
#     db.commit()
#     db.refresh(comment)
    
    
#     return comment



