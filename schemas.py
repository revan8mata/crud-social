
from typing import Literal

from pydantic import BaseModel, EmailStr

class login(BaseModel):
    username: str
    password: str


class create_account_res(BaseModel):
    username: str

class vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]

class create_account(BaseModel):
    password: str
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    id: int | None = None


class delete(BaseModel):
    username: str

class update_account(BaseModel):
    pass


    class Config:
        from_attributes = True



class post(BaseModel):
    content : str

    class Config:
        from_attributes = True



class update_user(BaseModel):
    username: str
    password: str
    email: EmailStr


class comment(BaseModel):
    content: str
    post_id: int
