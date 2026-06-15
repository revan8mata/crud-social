import models
from alembic.autogenerate.compare import comments
from fastapi import HTTPException
from sqlalchemy.testing.pickleable import User

ROUTER = APIRouter(
    tags=["comments"],
    prefix="/comments"
)



# @app.post("/posts/{id}/comments")
# async def coments(id: int ,comment: schemas.comment, db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
#     post = db.execute(select(models.Post).where(models.Post.id == id)).first()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)
#     upload = models.Comment(
#         **comment.model_dump(),
#         post_id=id,
#         user_id=current_user.id
#     )
#     db.add(upload)
#     db.commit()
#     db.refresh(upload)
#     return {"comment": upload.content}



