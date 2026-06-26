from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    if not password.strip():
        raise ValueError("Password Cannot Be Empty.")
    
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not (plain_password.strip() and hashed_password.strip()):
        raise ValueError("Plain password and hashed password cannot be empty.")
    
    return pwd_context.verify(plain_password, hashed_password)