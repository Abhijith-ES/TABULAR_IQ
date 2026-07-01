from sqlalchemy.orm import Session
from sqlalchemy import select, desc

from src.database.models import QueryHistory

def get_chat_history(db: Session, chat_id: int, limit: int=5) -> list[dict]:
    stmt = (
        select(QueryHistory)
        .where(QueryHistory.chat_id==chat_id)
        .order_by(desc(QueryHistory.created_at))
        .limit(limit)
    )

    exchanges = db.execute(stmt).scalars().all()

    exchanges.reverse() 
    
    return [
        {
            "query": exchange.query,
            "answer": exchange.answer
        }
        for exchange in exchanges
    ]
