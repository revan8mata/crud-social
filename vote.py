from fastapi import  FastAPI, Depends, Body, HTTPException, status, Response , APIRouter
import schemas
import database
import models
import oauth2
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from sqlalchemy.sql.functions import current_user
from sqlalchemy import func
from typing import Optional
ROUTER = APIRouter(
    tags=["vote"],
    prefix="/vote",
)

@ROUTER.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.vote,db: Session = Depends(get_db),
         current_user: int = Depends(oauth2.get_current_user)):
    ss = db.execute(select(models.Post)
          .where(models.Post.id == vote.post_id)
                    ).scalars().first()
    if not ss:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {vote.post_id} does not exist")

    found_query = db.execute(select(models.vote)
    .where(models.vote.post_id == vote.post_id,models.vote.user_id == current_user.id)).scalars().first()

    if vote.dir == 1:
        if found_query:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="This vote already exists")
        else:
            plusvote = models.vote(post_id = vote.post_id,user_id = current_user.id)
            db.add(plusvote)
            db.commit()
            return {"message": "Vote created successfully"}

        if not found_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)
        else:
            found_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "Vote deleted successfully"}


# @ROUTER.get("/user/postcount/{id}")
# async def user_postcount(id: int,offset :int = 0,limit: int=10, db: Session = Depends(get_db)):
#     trash = (db.execute(select(models.register.id,models.register.username,func.count(models.Post.id))
#                         .outerjoin(models.Post, models.Post.user_id == models.register.id)
#                         .group_by(models.register.id).where(models.register.id == id)).first())
#
#     return {"id": trash[0], "username": trash[1], "post_count": trash[2]}


# @ROUTER.get("/user/postcount/pages/{id}")
# async def user_postcount(id: int,
#                          search: Optional[str] = "" ,
# offset :int = 0,
# limit: int=10 ,
# db: Session = Depends(get_db)):
#     trash = (db.execute(select(models.register.id,models.register.username,func.count(models.Post.id))
#                         .outerjoin(models.Post, models.Post.user_id == models.register.id)
#                         .group_by(models.register.id).where(models.register.id == id).limit(limit).offset(offset).all()))





