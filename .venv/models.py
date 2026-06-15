from enum import unique
from sqlalchemy import DateTime
from fastapi.openapi.models import Schema
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from pydantic_core.core_schema import nullable_schema
from database import base
from sqlalchemy.orm import foreign
from sqlalchemy.sql import func

class Post(base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, nullable=False)

    username = Column(String)

    content = Column(String,nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),nullable=False)




class register(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)

    password = Column(String,nullable=False)
    username = Column(String,nullable=False,unique=True,)
    email = Column(String,nullable=False,unique=True)

    is_active = Column(Boolean,default=False,nullable=False)


class vote(base):
    __tablename__ = 'votes'
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)


# added mid project via alembic
class Comment(base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)

    content = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)


# comments
# --------
# id          (PK)
# content     (text)
# created_at  (timestamp)
#
# post_id     (FK → posts.id)
# user_id     (FK → users.id)