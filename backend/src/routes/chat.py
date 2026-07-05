from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.dependencies.auth import get_current_user
from src.services.chat_service import create_chat, process_query, get_full_chat_history, get_user_chats
from src.schemas.chat_schema import CreateChatRequest, CreateChatResponse, QueryRequest
from src.database.models import User


router = APIRouter(
    prefix='/chats',
    tags=["Chat Router"]
)

@router.post("", response_model=CreateChatResponse)
def create_new_chat(
    request_data: CreateChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    try:
        new_chat = create_chat(
            db=db,
            current_user=current_user,
            dataset_id=request_data.dataset_id
        )

        return CreateChatResponse(
            chat_id=new_chat.id,
            title=new_chat.title
            )
    
    except ValueError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e)
        )
    
@router.post('/{chat_id}/query')
def process_user_query(
    chat_id: int,
    user_query: QueryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ):

    try:
        formatted_llm_response = process_query(
            db=db,
            current_user=current_user,
            chat_id=chat_id,
            user_query=user_query.query
        )

        return formatted_llm_response
    
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    
@router.get("")
def user_chats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        user_chats_info = get_user_chats(current_user=current_user, db=db)
        return user_chats_info
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@router.get("/{chat_id}/history")
def get_chat_history(chat_id: int,
                     current_user: User = Depends(get_current_user),
                     db: Session = Depends(get_db)):
    try:
        chat_history = get_full_chat_history(
            current_user=current_user,
            db=db,
            chat_id=chat_id
            )
        
        return chat_history
    
    except ValueError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e)
        )