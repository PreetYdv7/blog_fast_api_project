from fastapi import FastAPI, Depends, HTTPException, status
import schema
from typing import List
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code = status.HTTP_201_CREATED)
def create_blog(request: schema.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete("/blog/{id}", status_code = status.HTTP_204_NO_CONTENT)
def destroy_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
    else:
        blog.delete()
    db.commit()


@app.put("/blog/{id}", status_code = status.HTTP_202_ACCEPTED)
def update(id: int, request: schema.Blog, db: Session = Depends(get_db)):
     blog = db.query(models.Blog).filter(models.Blog.id == id).first()
     if not blog:
         raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
     else:
         blog.title = request.title
         blog.body = request.body
     db.commit()
     return blog


@app.get("/blogs", response_model = List[schema.ShowBlog])
def read_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blog/{id}", status_code = status.HTTP_200_OK, response_model=schema.ShowBlog)
def read_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
    else:
        return blog

