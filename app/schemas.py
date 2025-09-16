from pydantic import BaseModel,EmailStr # Schema validation with pydantic
from datetime import datetime
from typing import Optional,Literal

class PostBase(BaseModel): # to set the schema
    # id:int
    title :str
    content :str
    published : bool = True


class CreatePost(PostBase):
    pass

class UserCreateResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config:
        orm_mode = True

class ResponsePost(PostBase): # to set the schema
    id:int
    createat: datetime 
    owner_id:int
    owner:UserCreateResponse

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    post:ResponsePost
    votes:int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email:EmailStr # email validator
    password:str



class UserLogin(BaseModel):
    email:EmailStr
    password:str

class TokenData(BaseModel):
    id:Optional[int] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class Vote(BaseModel):
    post_id:int
    dir:Literal[0,1]

