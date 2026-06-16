import utilities
import schemas
import models
import oauth2
from fastapi import Cookie, FastAPI, Depends, Body, HTTPException, status, Response , APIRouter
from logging import exception
from sqlalchemy.orm import Session
from database import get_db

ROUTER = APIRouter(
    tags=["users"],
)

@ROUTER.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.create_account_res)
async def post(user : schemas.create_account , db: Session = Depends(get_db)):
# hash that shit - user.password
    hash3d = utilities.hash(user.password)
    user.password = hash3d

    existing = db.query(models.register).filter(models.register.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"username {user.username} already taken")
    newposta = models.register(**user.model_dump())
    db.add(newposta)
    db.commit()
    db.refresh(newposta)
    return newposta

# route- creation input validation- hash operation-
# db dependenct and selection via orm  - confirm existance - add to db- commit to db - export

@ROUTER.get("/user/{id}")
async def searchbyid(id: int, db: Session = Depends(get_db)):
    tg = db.query(models.register).filter(models.register.id==id).first()
    if tg == None:
        raise HTTPException(status_code=404, detail=f"id of {id} does not exist")
    return tg



# delete account
@ROUTER.delete("/user/delete/{user_id}")
async def delete(user_id: int, db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    delacc = db.query(models.register).filter(models.register.id==user_id).first()
    if delacc == None:
        raise HTTPException(status_code=404, detail=f"id of {user_id} does not exist")
    db.delete(delacc)
    db.commit()
    return {"message" : "DELETED" }

@ROUTER.put("/user")
async def put(update_user : schemas.update_user, db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    updateacc = db.query(models.register).filter(models.register.id==current_user.id)
    if updateacc.first() == None:
        raise HTTPException(status_code=404, detail=f"id of {current_user.id} does not exist")
    updateacc.update(update_user.model_dump(),synchronize_session=False)
    db.commit()

    return {"message" : "UPDATED" }


