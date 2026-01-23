from fastapi import FastAPI
from models import Base
from routers import blog, user
from database import engine


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(blog.router)
app.include_router(user.router)
