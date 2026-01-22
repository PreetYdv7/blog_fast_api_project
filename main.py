from fastapi import FastAPI, Depends, HTTPException, status
import schema
from typing import List
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code = status.HTTP_201_CREATED, tags = ["Blog"])
def create_blog(request: schema.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete("/blog/{id}", status_code = status.HTTP_204_NO_CONTENT, tags = ["Blog"])
def destroy_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
    db.delete(blog)
    db.commit()


@app.put("/blog/{id}", status_code = status.HTTP_202_ACCEPTED, tags = ["Blog"])
def update(id: int, request: schema.Blog, db: Session = Depends(get_db)):
     blog = db.query(models.Blog).filter(models.Blog.id == id).first()
     if not blog:
         raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
     else:
         blog.title = request.title
         blog.body = request.body
     db.commit()
     return blog


@app.get("/blogs", response_model = List[schema.ShowBlog], tags = ["Blog"])
def read_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blog/{id}", status_code = status.HTTP_200_OK, response_model=schema.ShowBlog, tags = ["Blog"])
def read_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
    return blog


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/user", response_model=schema.ShowUser, tags = ["User"])
def create_user(request: schema.User, db: Session = Depends(get_db)):
    hashed_password = pwd_cxt.hash(request.password)
    new_user = models.User(username = request.username, email = request.email, password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/user/{id}", response_model = schema.ShowUser, tags = ["User"])
def read_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    return user


