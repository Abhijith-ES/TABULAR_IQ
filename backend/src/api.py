from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from src.services.auth_service import register_user
from src.database.db import get_db
from src.schemas import RegisterRequest

app = FastAPI()

@app.get('/')
def home():
    return {
        "message": "TabularIQ Is Running!"
    }

@app.get('/health')
def health_check():
    return {
        "status": "Healthy"
    }

@app.post('/register')
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