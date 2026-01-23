from fastapi import APIRouter, Depends, HTTPException, status
from schemas import schema
import database
from models import Blog, User
from typing import List
from sqlalchemy.orm import Session, joinedload


router = APIRouter(
    prefix="/blog",
    tags=["Blog"]
)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_blog(request: schema.Blog, db: Session = Depends(database.get_db)):
    # Verify user exists
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {request.user_id} not found")
    
    new_blog = Blog(title=request.title, body=request.body, user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy_blog(id: int, db: Session = Depends(database.get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
    
    db.delete(blog)
    db.commit()


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schema.Blog, db: Session = Depends(database.get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
    
    # Verify user exists if user_id is being changed
    if request.user_id != blog.user_id:
        user = db.query(User).filter(User.id == request.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User with id {request.user_id} not found")
    
    blog.title = request.title
    blog.body = request.body
    blog.user_id = request.user_id
    db.commit()
    db.refresh(blog)
    return blog


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schema.ShowBlog)
def read_blog(id: int, db: Session = Depends(database.get_db)):
    # Load owner relationship to avoid lazy loading issues
    blog = db.query(Blog).options(joinedload(Blog.owner)).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
    return blog


@router.get("/blogs", response_model=List[schema.ShowBlog])
def read_blogs(db: Session = Depends(database.get_db)):
    # Load owner relationship to avoid lazy loading issues
    blogs = db.query(Blog).options(joinedload(Blog.owner)).all()
    return blogs