from typing import List, Literal, Optional, TypeAlias,Union
from pydantic import BaseModel, Required

class ResponseFormat(BaseModel):
    type:str = "json_object"

   

class ChatCompletionContentPartTextParam(BaseModel):
    text: str
    """The text content."""

    type: str = "text"
    """The type of the content part."""


class ImageURL(BaseModel):
    url: str
    """Either a URL of the image or the base64 encoded image data."""

class ChatCompletionContentPartImageParam(BaseModel):
    image_url: ImageURL

    type: str = "image_url"
    """The type of the content part."""


ChatCompletionContentPartParam: TypeAlias = Union[
    ChatCompletionContentPartTextParam, ChatCompletionContentPartImageParam
]


class ChatCompletionSystemMessageParam(BaseModel):
    content: str
    """The contents of the system message."""

    role: str = "system"
    """The role of the messages author, in this case `system`."""

class ChatCompletionUserMessageParam(BaseModel):
    content: Union[str, List[ChatCompletionContentPartParam]]
    """The contents of the user message."""

    role: str = "user"
    """The role of the messages author, in this case `user`."""


class ChatCompletionAssistantMessageParam(BaseModel):
    role: str = "assistant"
    """The role of the messages author, in this case `assistant`."""

    content: str =""
    """The contents of the assistant message.

    """

__all__ = ["ChatCompletionMessageParam"]
    
ChatCompletionMessageParam: TypeAlias = Union[
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam
]
class ChatMessage(BaseModel):
    model: str = "llama-3.2-90b-vision-preview"
    max_tokens: int = 2500
    response_format: ResponseFormat = ResponseFormat()
    messages: List[ChatCompletionMessageParam]
    
 