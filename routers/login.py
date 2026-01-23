from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import schema
from models import models
from database import get_db
from routers import token
from hashing import Hash

router = APIRouter(
    tags=['login'],
    prefix='/login',
)

@router.post("/login")
def login(request: schema.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect username or password"
        )
    if not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect username or password"
        )
    access_token = token.create_access_token(
        data={"sub": user.email} )
    return {"access_token": access_token, "token_type": "bearer"}