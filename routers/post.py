from math import acosh

import schemas
import models
from fastapi import  FastAPI, Depends, Body, HTTPException, status, Response , APIRouter
import oauth2
from logging import exception
from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy.sql.functions import current_user
from sqlalchemy import func
ROUTER = APIRouter(
    tags=["post"],
)
# @ROUTER.get("/post/likesall"):
# acync def get_likes(db: session = depends(get_db)):
# bullshit=db.query(models.Post).filter(models.Post.user_id == votes.post_id)

@ROUTER.get("/post/all")          #will add a response model
async def get_posts(id: int ,db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    holy = db.query(models.Post).filter(models.Post.user_id==current_user.id).all()
    return holy

@ROUTER.get("/post/single")
async def get_posts(post_id : int,db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(
        models.Post.id == post_id,
        models.Post.user_id == current_user.id
    ).first()
    return post



# post = db.execute(select(models.Post).where(models.Post.user_id==current_user.id)).first
#     return post
# )


@ROUTER.post("/post", status_code=status.HTTP_201_CREATED )
async def create_post( post : schemas.post,db: Session = Depends(get_db), current_user : schemas.TokenData = Depends(oauth2.get_current_user) ):
    upload = models.Post(
        **post.model_dump(),
        user_id=current_user.id
    )
    db.add(upload)
    db.commit()
    db.refresh(upload)
    return upload

@ROUTER.delete("/post/{id}" ,status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):

    holy = db.query(models.Post).filter(models.Post.id==id)
    deletable = holy.first()
    if deletable is None:
        raise HTTPException(status_code=404, detail=f"id of {id} does not exist")
    if current_user.id != deletable.user_id:
        raise HTTPException(status_code=403, detail="not authorized to delete this post")

    holy.delete(synchronize_session=False)
    db.commit()


@ROUTER.put("/post/{id}")
async def put(id : int ,user : schemas.post ,db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    holy = db.query(models.Post).filter(models.Post.id == id)
    if holy.first() is None:
        raise HTTPException(status_code=404, detail=f"id of {id} does not exist")
    if current_user.id != holy.first().user_id:
        raise HTTPException(status_code=403, detail="not authorized to update this post")
    holy.update({**user.model_dump()}, synchronize_session=False)
    db.commit()
    return {"data": holy.first()}


# def erg(db: Session = Depends(get_db),limit: int = 10,offset: int = 0,search: Optional[str] = ""):
#     db.query(models.Post.content).filter(models.Post.content.contain(search)).limit(limit).offset(offset).all()
#
#     results = (db.query(models.Posts, func.count.models.post_id)
#                .join(models.Votes, models.Votes.posts_id == models.Posts.id,isouter=True)
#                .group_by(models.Posts.id).all())
# posts =db.query(models.Post).filter(models.Post.user_id == current_user.id).all()

