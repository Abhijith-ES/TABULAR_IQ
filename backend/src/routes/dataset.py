from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session

from src.dependencies.auth import get_current_user
from src.database.db import get_db
from src.database.models import User
from src.services.dataset_service import get_user_datasets, upload_dataset
from src.schemas.dataset_schema import UploadResponse


router = APIRouter(
    prefix = "",
    tags = ["Database Router"]
)

@router.get("/datasets")
def user_datasets(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        dataset_info = get_user_datasets(current_user=current_user, db=db)
        return dataset_info
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@router.post("/datasets/upload", response_model=UploadResponse)
def upload_user_dataset(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    file: UploadFile = File(...)):

    try:
        dataset = upload_dataset(
            current_user=current_user,
            db=db,
            file=file)
        
        return UploadResponse(
            id=dataset.id,
            file_name=dataset.file_name,
            uploaded_at=dataset.uploaded_at
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )