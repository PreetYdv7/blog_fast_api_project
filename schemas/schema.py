from pydantic import BaseModel
from typing import List, Optional


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):
    user_id: int
    
    model_config = {
        "from_attributes": True
    }


class User(BaseModel):
    username: str
    email: str
    password: str


# Separate schemas to prevent infinite loops when showing relationships
class UserInBlog(BaseModel):
    id: int
    username: str
    email: str
    
    model_config = {
        "from_attributes": True
    }


class BlogInUser(BaseModel):
    id: int
    title: str
    body: str
    
    model_config = {
        "from_attributes": True
    }


class ShowUser(BaseModel):
    id: int
    username: str
    email: str
    blogs: List[BlogInUser] = []
    
    model_config = {
        "from_attributes": True
    }


class ShowBlog(BaseModel):
    id: int
    title: str
    body: str
    owner: Optional[UserInBlog] = None
    
    model_config = {
        "from_attributes": True
    }

class Login(BaseModel):
    username: str
    password: str

    model_config = {
        "from_attributes": True
    }


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
