from fastapi import HTTPException,status,Depends,APIRouter
from fastapi.responses import JSONResponse
from typing import List,Optional
from app import models,schemas,oauth2
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy import func

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)




# @router.get("/",response_model=List[schemas.PostOut])
@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db:Session = Depends(get_db),current_user : int =Depends(oauth2.get_current_user),
              limit:int =10,skip:int=0,search:Optional[str]=""):
    # posts = post.dict()
    # cursor.execute(""" SELECT * FROM POSTS """)
    # posts=cursor.fetchall()
    # print(search)
    # posts=db.query(models.Post).filter((models.Post.owner_id == current_user.id) & (models.Post.title.contains(search))).limit(limit).offset(skip).all() 
    results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id==models.Post.id,isouter=True) .group_by(
            models.Post.id).filter((models.Post.owner_id == current_user.id) & (models.Post.title.contains(search))).limit(
                limit).offset(skip).all() 

    print(results)
    return [{"post": post, "votes": votes} for post, votes in results]
    # return results

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.ResponsePost)
# def create_post(payload:dict=Body(...)):
#     print(payload)
#     return{"new_posts":f"title:{payload.get('title') } content:{payload.get('content')}"}

    # post_dict = new_post.dict()
    # post_dict['id']=randrange(1,100000)
    # my_post.append(post_dict)
    # print(new_post.rating)
    # cursor.execute(""" INSERT INTO POSTS (title,content,published) VALUES (%s,%s,%s)""",
    #                (new_post.title,new_post.content, new_post.published))
    # # new_post = cursor.fetchone()
    # connection.commit()
def create_post(post:schemas.CreatePost,db:Session=Depends(get_db),
                current_user : schemas.UserCreateResponse =Depends(oauth2.get_current_user)
                ):
    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def find_post_by_id(id):
    for p in my_post:
        if p['id'] == id:
            return p

@router.get("/{id}",response_model=schemas.PostOut)
def get_post_by_id(id:int,db:Session=Depends(get_db),current_user : int =Depends(oauth2.get_current_user)):
    # post=find_post_by_id(id)
    # cursor.execute(""" SELECT * FROM POSTS WHERE ID=%s """,(id,))
    # post=cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"the request with id: {id} was not found")
    print(current_user.email)
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id==models.Post.id,isouter=True) .group_by(
            models.Post.id).filter(models.Post.id == id).first()
    if not post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"the request with id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"Not authorized to perform the requested action")
    print(post)
    return post
    # return Response(status_code=status.HTTP_201_CREATED)

def find_post_index(id):
     for i,p in enumerate(my_post):
        if p['id'] == id:
            return i
        
@router.delete("/{id}")
def delete_post(id:int,db:Session=Depends(get_db),current_user : int =Depends(oauth2.get_current_user)):
    # post_index = find_post_index(id)
    # cursor.execute(""" DELETE FROM POSTS WHERE ID=%s """,(id,))
    # connection.commit()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"the post with id: {id} was not found")
    # my_post.pop(post_index)
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"Not authorized to perform the requested action")
    db.delete(post)
    db.commit()
    # db.refresh(post)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT,content={"message":"Item deleted successfully"})

@router.put("/{id}",response_model=schemas.ResponsePost)
def update_post(id:int,post:schemas.CreatePost,db:Session=Depends(get_db),current_user : int =Depends(oauth2.get_current_user)):
    print(id)
    # post_index = find_post_index(id)
    # cursor.execute(""" SELECT * FROM POSTS WHERE ID=%s """,(id,))
    # existing_post = cursor.fetchone()

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    # if not existing_post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"the post with id: {id} was not found")
    # post_dict = post.dict()
    # post_dict['id']=id
    # # my_post[post_index] = post_dict
    # update_query=""" UPDATE POSTS SET title =%s, content=%s,published=%s WHERE id=%s"""
    # cursor.execute(update_query,(post.title,post.content,post.published,id))
    # connection.commit()

    # #fetch the updated record
    # cursor.execute(""" SELECT * FROM POSTS WHERE ID=%s """,(id,))
    # updated_post = cursor.fetchone()
    # print(updated_post)
    # return {"message":"Updated the post successfully","data":updated_post}

    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"the post with id: {id} was not found")
    post_query.update(post.dict(),synchronize_session=False)
    if existing_post.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"Not authorized to perform the requested action")
    db.commit()


    return post_query.first()
