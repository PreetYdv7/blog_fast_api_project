from fastapi import APIRouter, Depends, HTTPException
import schema
import database
import models
from sqlalchemy.orm import Session, joinedload
from passlib.context import CryptContext


router = APIRouter(
    prefix="/user",
    tags=["User"]
)


# Password hashing context
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("", response_model=schema.ShowUser)
def create_user(request: schema.User, db: Session = Depends(database.get_db)):
    # Hash password before storing
    hashed_password = pwd_cxt.hash(request.password)
    new_user = models.User(username=request.username, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schema.ShowUser)
def read_user(id: int, db: Session = Depends(database.get_db)):
    # Load blogs relationship to avoid lazy loading issues
    user = db.query(models.User).options(joinedload(models.User.blogs)).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    return user
