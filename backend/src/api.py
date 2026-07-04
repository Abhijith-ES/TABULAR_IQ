from fastapi import FastAPI
from src.routes import auth
from src.routes import chat

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

app.include_router(auth.router)
app.include_router(chat.router)