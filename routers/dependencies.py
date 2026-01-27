from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from routers.token import verify_token
from sqlalchemy.orm import Session
from database import get_db
from models import User

security = HTTPBearer()

def get_current_user(token: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = token.credentials
    token_data = verify_token(token, credentials_exception)
    user = db.query(User).filter(User.email == token_data.email).first()
    return user





