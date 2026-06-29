from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.database.db import get_db
from src.database.models import User
from src.utils.jwt_handler import verify_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
        )-> User:
    
    payload = verify_access_token(token)

    user_id = payload.get('sub')

    if not user_id:
        raise ValueError("Invalid Token Payload")
    
    user_id = int(user_id)
    
    stmt = select(User).where(User.id==user_id)
    current_user = db.execute(stmt).scalars().first()

    if not current_user:
        raise ValueError("No User Found.")
    
    return current_user