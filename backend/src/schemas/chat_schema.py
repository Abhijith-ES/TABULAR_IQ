from pydantic import BaseModel, Field


class CreateChatRequest(BaseModel):
    dataset_id : int = Field(gt=0)


class CreateChatResponse(BaseModel):
    chat_id : int
    title : str


class QueryRequest(BaseModel):
    query: str = Field(
        min_length=1,
        max_length=1000
    )


class RenameRequest(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=100
    )


class RenameResponse(BaseModel):
    id: int
    title: str