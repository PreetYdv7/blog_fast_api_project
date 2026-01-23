from fastapi import APIRouter, Depends, HTTPException, status
from schemas import schema
import database
from models import Blog, User
from typing import List
from sqlalchemy.orm import Session, joinedload
from routers import oauth2

router = APIRouter(
    prefix="/blog",
    tags=["Blog"]
)

# ---------------- CREATE BLOG (JWT PROTECTED) ----------------
@router.post("", status_code=status.HTTP_201_CREATED)
def create_blog(
    request: schema.Blog,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(oauth2.get_current_user)
):
    new_blog = Blog(
        title=request.title,
        body=request.body,
        user_id=current_user.id   # ✅ user comes from JWT
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# ---------------- GET ALL BLOGS (JWT PROTECTED) ----------------
@router.get("/blogs", response_model=List[schema.ShowBlog])
def read_blogs(
    db: Session = Depends(database.get_db),
    current_user: User = Depends(oauth2.get_current_user)
):
    blogs = db.query(Blog).options(joinedload(Blog.owner)).all()
    return blogs


# ---------------- GET SINGLE BLOG ----------------
@router.get("/{id}", response_model=schema.ShowBlog)
def read_blog(
    id: int,
    db: Session = Depends(database.get_db)
):
    blog = db.query(Blog).options(joinedload(Blog.owner))\
        .filter(Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    return blog


# ---------------- UPDATE BLOG (OWNER ONLY) ----------------
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(
    id: int,
    request: schema.Blog,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(oauth2.get_current_user)
):
    blog = db.query(Blog).filter(Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    if blog.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)
    return blog


# ---------------- DELETE BLOG (OWNER ONLY) ----------------
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(oauth2.get_current_user)
):
    blog = db.query(Blog).filter(Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    if blog.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(blog)
    db.commit()
