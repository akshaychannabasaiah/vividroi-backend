from typing import List
from pydantic import BaseModel

    
class Content(BaseModel):
    type: str
    
class TextContent(Content):
    text: str
    
class ImageUrl(BaseModel):
    url: str

class ImageContent(Content):
    image_url: List[ImageUrl]    
        
class MessageContent(BaseModel):
    role: str
    content: Content