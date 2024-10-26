from typing import List
from pydantic import BaseModel

from app.model.ChatMessageModel import ChatCompletionMessageParam

class AnalysisTable(BaseModel):
    xlabel: str
    ylabel: str
    values: dict

class CampaignAnalysis(BaseModel):
    name: str
    table :AnalysisTable
    observation:str
    recommendation:str
    
class CampaignAnalysisResponse(BaseModel):
    messages: List[ChatCompletionMessageParam]
    analysis: List[CampaignAnalysis]