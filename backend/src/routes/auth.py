from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from src.services.auth_service import register_user, login_user
from src.database.db import get_db
from src.schemas.auth_schema import RegisterRequest, LoginRequest
from src.utils.jwt_handler import create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication Router"]
)

@router.post('/register')
def register_new_user(user_data: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = register_user(db=db, user_data=user_data)
        return {
            "status": "User Added Successfully.",
            "user_id": user.id,
            "user_name": user.name,
            "created_at": user.created_at
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )
    
@router.post('/login')
def login_existing_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = login_user(
            login_data=login_data,
            db=db)
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
    
    payload = {
        'sub' : str(user.id)
    }

    token = create_access_token(payload)

    return {
        "access_token": token,
        "token_type": "bearer"
    }