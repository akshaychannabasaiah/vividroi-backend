from typing import List
from app.model.MessageModel import MessageContent
from pydantic import BaseModel

class ChatMessage(BaseModel):
    model: str
    max_tokens: int
    response_format: str
    messages: List[MessageContent]