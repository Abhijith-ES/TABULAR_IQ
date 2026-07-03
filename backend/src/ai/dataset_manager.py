import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone

from src.database.models import ChatSession, Dataset


class DatasetManager:
    def __init__(self):
        self._cache = {}

    def load_dataset(self, chat_id: int, db: Session):
        if chat_id in self._cache:
            self._cache[chat_id]["last_accessed"] = datetime.now(timezone.utc)
            return self._cache[chat_id]["dataframe"]
        
        try:
            stmt = select(ChatSession).where(ChatSession.id==chat_id)
            result = db.execute(stmt).scalars().first()

            if result is None:
                raise ValueError("Chat Not Found.")

            stmt_dataset = select(Dataset).where(Dataset.id==result.dataset_id)
            dataset = db.execute(stmt_dataset).scalars().first()

            if dataset is None:
                raise ValueError("Dataset Not Found.")
            
        except SQLAlchemyError as e:
            raise

        df = pd.read_csv(dataset.file_path)

        self._cache[chat_id] = {
            "dataframe": df,
            "dataset_id": dataset.id,
            "user_id": dataset.user_id,
            "loaded_at": datetime.now(timezone.utc),
            "last_accessed": datetime.now(timezone.utc)
        }

        return df