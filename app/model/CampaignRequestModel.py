from typing import List
from pydantic import BaseModel

from app.model.ChatMessageModel import ChatCompletionMessageParam
from app.model.PersonaModel import Persona

class CampaignRequest(BaseModel):
    messages: List[ChatCompletionMessageParam]
    name: str
    objective: str
    img :str