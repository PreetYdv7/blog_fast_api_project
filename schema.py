from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str

class ShowBlog(BaseModel):
    title: str
    body: str
    model_config = {
        "from_attributes": True
    }

class User(BaseModel):
    username: str
    email: str
    password: str

class ShowUser(BaseModel):
    username: str
    email: str
    model_config = {
        "from_attributes": True
    }