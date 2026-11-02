from datetime import datetime
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, example="I have fever and cough")


class ChatResponse(BaseModel):
    response: str


class ChatHistoryOut(BaseModel):
    id: int
    user_id: int
    user_message: str
    ai_response: str
    timestamp: datetime

    class Config:
        from_attributes = True
