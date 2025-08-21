from pydantic import BaseModel
from typing import Optional

# Successful response ke liye schema
class ChatResponse(BaseModel):
    audio_url: str
    user_query_text: str
    llm_response_text: str

# Error response ke liye schema
class ErrorResponse(BaseModel):
    error: str
    audio_url: Optional[str] = None
