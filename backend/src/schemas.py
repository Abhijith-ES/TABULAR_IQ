import re
from pydantic import BaseModel, Field, EmailStr, field_validator


class RegisterRequest(BaseModel):
    name : str = Field(..., min_length=1, max_length=50)
    email : EmailStr
    password : str = Field(..., min_length=8, max_length=128)

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v:str) -> str:
        PASSWORD_PATTERN = re.compile(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$"
        )
        if not v.strip():
            raise ValueError(
                "Password Cannot Be Empty."
            )

        if not PASSWORD_PATTERN.fullmatch(v):
            raise ValueError(
                "Password must contain at least one uppercase letter,"
                "one lowercase letter, one digit, and one special character."
            )
        
        return v