from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.database.models import ChatSession, QueryHistory, User, Dataset
from src.ai.dataset_manager import DatasetManager
from src.ai.metadata_extractor import extract_metadata
from src.ai.conversation_history import get_chat_history
from src.ai.prompt_builder import build_prompt
from src.ai.llm_service import generate_code
from src.ai.code_executor import execute_code
from src.ai.response_formatter import format_response


dataset_manager = DatasetManager()

def create_chat(db: Session, current_user: User, dataset_id: int) -> ChatSession:
    stmt = (
        select(Dataset)
        .where(Dataset.user_id==current_user.id,
               Dataset.id==dataset_id)
    )
    dataset = db.execute(stmt).scalars().first()

    if dataset is None:
        raise ValueError("Access Denied.")

    new_chat = ChatSession(
        user_id=current_user.id,
        dataset_id=dataset.id,
    )

    try:
        db.add(new_chat)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise

    db.refresh(new_chat)

    return new_chat

def process_query(db:Session, current_user: User, chat_id: int, user_query: str) -> dict:
    stmt = (
        select(ChatSession)
        .where(ChatSession.id==chat_id,
               ChatSession.user_id==current_user.id)
    )

    current_chat = db.execute(stmt).scalars().first()

    if current_chat is None:
        raise ValueError("Chat not found or access denied.")

    df = dataset_manager.load_dataset(
        chat_id=current_chat.id,
        db=db
    )

    metadata = extract_metadata(df=df)
    chat_history = get_chat_history(
        db=db, 
        chat_id=current_chat.id)
    
    prompt = build_prompt(metadata=metadata,
                          chat_history=chat_history,
                          user_query=user_query)

    generated_code = generate_code(prompt=prompt)

    result = execute_code(code=generated_code, df=df)

    execution_response = format_response(
        execution_result=result["result"],
        execution_time_ms=result["execution_time_ms"]
        )
    
    query_transaction = QueryHistory(
        chat_id=current_chat.id,
        query=user_query,
        answer=str(execution_response),
        generated_code=generated_code,
        execution_time_ms=result["execution_time_ms"]
    )

    if current_chat.title=="New Chat":
        current_chat.title=user_query[:50]

    try:
        db.add(query_transaction)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise

    return execution_response

def get_user_chats(current_user: User, db: Session):
    stmt = (
        select(ChatSession)
        .where(ChatSession.user_id==current_user.id)
        .order_by(desc(ChatSession.updated_at))
    )

    user_chats = db.execute(stmt).scalars().all()

    chat_info = []

    for chat in user_chats:
        chat_info.append(
            {
                "id": chat.id,
                "title": chat.title,
                "updated_at": chat.updated_at
            }
        )
    
    return chat_info

def get_full_chat_history(current_user: User, db: Session, chat_id: int):
    chat_stmt = (
        select(ChatSession)
        .where(ChatSession.id==chat_id, ChatSession.user_id==current_user.id)
    )

    current_chat = db.execute(chat_stmt).scalars().first()

    if current_chat is None:
        raise ValueError("Chat not found or access denied.")
    
    history_stmt = (
        select(QueryHistory)
        .where(QueryHistory.chat_id==current_chat.id)
        .order_by(QueryHistory.created_at)
    )

    chat_history = db.execute(history_stmt).scalars().all()
    
    history_info = []

    for exchanges in chat_history:
        history_info.append(
            {
                "id": exchanges.id,
                "query": exchanges.query,
                "answer": exchanges.answer,
                "generated_code": exchanges.generated_code,
                "created_at": exchanges.created_at
            }
        )

    return history_info

def rename_chat(current_user: User, db: Session, chat_id: int, title: str):
    stmt = (
        select(ChatSession)
        .where(ChatSession.id==chat_id,
               ChatSession.user_id==current_user.id)
    )

    current_chat = db.execute(stmt).scalars().first()

    if current_chat is None:
        raise ValueError("Chat does not exist!")
    
    current_chat.title = title

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise

    db.refresh(current_chat)

    return current_chat