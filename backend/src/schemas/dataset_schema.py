from pydantic import BaseModel
from datetime import datetime


class UploadResponse(BaseModel):
    id: int
    file_name: str
    uploaded_at: datetime