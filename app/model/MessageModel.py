from typing import List, Union
from pydantic import BaseModel, Field

    
# class Content(BaseModel):
#     type: str
    
# class TextContent(Content):
#     text: str
    
# class ImageUrl(BaseModel):
#     url: str

# class ImageContent(Content):
#     image_url: ImageUrl
        
# class MessageContent(BaseModel):
#     role: str
#     content: Union[List[Content], str] = Field(union_mode='left_to_right')