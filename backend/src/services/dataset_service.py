from fastapi import UploadFile
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
import shutil
from pathlib import Path
import pandas as pd
import uuid

from src.database.models import User, Dataset

backend_root = Path(__file__).resolve().parents[2]
upload_dir = backend_root / "uploads"

upload_dir.mkdir(parents=True, exist_ok=True)

def upload_dataset(db: Session, current_user: User, file: UploadFile) -> Dataset:
    # Validation Of Input File:
    allowed_content_types = [
        'text/csv',
        'application/csv', 
        'application/vnd.ms-excel'
    ]
    if (
        not file.filename.lower().endswith('.csv')
        or file.content_type not in allowed_content_types
    ):
        raise ValueError("Invalid File Format")
    
    # Setting up the Directory For File Storage
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    user_upload_dir= upload_dir / f"user_{current_user.id}" 
    user_upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = user_upload_dir / unique_filename

    try:
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
    except OSError:
        raise ValueError("Failed to Save File.")

    # Validating the content:
    try:
        pd.read_csv(file_path, nrows=5)
    except Exception:
        if file_path.exists():
            file_path.unlink()
        raise ValueError("Invalid File Type.")

    # Creating an instance of Dataset Model
    dataset = Dataset(
        user_id=current_user.id,
        file_name=file.filename,
        file_path=str(file_path)
    )

    try: 
        db.add(dataset)
        db.commit()

        db.refresh(dataset)

    except SQLAlchemyError as e:
        db.rollback()
        if file_path.exists():
            file_path.unlink()
        raise
    
    return dataset

def get_user_datasets(current_user: User, db: Session):
    stmt = (
        select(Dataset)
        .where(Dataset.user_id==current_user.id)
    )

    datasets = db.execute(stmt).scalars().all()

    dataset_info = []

    for dataset in datasets:
        dataset_info.append(
            {
                "id": dataset.id,
                "name": dataset.file_name,
                "uploaded_at": dataset.uploaded_at
            }
        )
    
    return dataset_info