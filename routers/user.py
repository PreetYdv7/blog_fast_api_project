from fastapi import APIRouter, Depends, HTTPException
from schemas import schema
import database
from models import User
from sqlalchemy.orm import Session, joinedload
from hashing import Hash


router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("", response_model=schema.ShowUser)
def create_user(request: schema.User, db: Session = Depends(database.get_db)):
    # Hash password before storing
    hashed_password = Hash.bcrypt(request.password)
    new_user = User(username=request.username, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schema.ShowUser)
def read_user(id: int, db: Session = Depends(database.get_db)):
    # Load blogs relationship to avoid lazy loading issues
    user = db.query(User).options(joinedload(User.blogs)).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    return user
