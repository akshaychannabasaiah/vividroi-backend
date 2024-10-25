from typing import List
from app.model.MessageModel import MessageContent
from pydantic import BaseModel

class ResponseFormat(BaseModel):
    type:str = "json_object"

class ChatMessage(BaseModel):
    model: str = "llama-3.2-90b-vision-preview"
    max_tokens: int = 2500
    response_format: ResponseFormat = ResponseFormat()
    messages: List[MessageContent]