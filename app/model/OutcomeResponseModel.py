from typing import List
from pydantic import BaseModel

from app.model.ChatMessageModel import ChatCompletionMessageParam
   
class Outcome(BaseModel):
    name:str
    description: str
    val: str
    

class OutcomeResponse(BaseModel):    
    outcomes: List[Outcome]
        
class OutcomeRequest(BaseModel):    
    messages: List[ChatCompletionMessageParam]