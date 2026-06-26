from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.schemas import RegisterRequest
from src.utils.security import hash_password
from src.database.models import User


def register_user(db: Session, user_data: RegisterRequest) -> User:
    # Checking whether there exists a User with Same Email
    stmt = select(User).where(User.email == user_data.email)

    existing_user = db.execute(stmt).scalars().first()

    if existing_user:
        raise ValueError("Email ID Already Exists, Please Login.")
    
    hashed_password = hash_password(user_data.password)
    
    user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_password
        )
    
    try:
        db.add(user)
        db.commit()

        db.refresh(user)

    except SQLAlchemyError as e:
        db.rollback()
        raise

    return user