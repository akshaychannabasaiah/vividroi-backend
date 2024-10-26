import json
from typing import List
import warnings
from app.chat.getGroqChat import GroqChat
from app.model.CampaignAnalysisModel import CampaignAnalysis, CampaignAnalysisResponse
from app.model.CampaignRequestModel import CampaignRequest
from app.model.PersonaModel import Persona, PersonaResponse
from app.model.PersonaRequestModel import PersonaRequest
from fastapi import Depends, APIRouter, Body, HTTPException 
from fastapi import BackgroundTasks 
from app.configuration.getConfig import Config


# get the config file
configuration = Config()

# SET THE API-ID: DO NOT CHANGE THIS!
API_ID = configuration.API_ID
API_VERSION = configuration.API_VERSION

groqChat = GroqChat()
# fastAPI Instance
router = APIRouter()

# Logger
logger = configuration.logger

@router.post("/chat/personas", tags=["Chat"], response_model=PersonaResponse)
async def personas(personaRequest: PersonaRequest = Body(None)):
    """
    Returns personas to the given attributes
    :param data:
    :return:
    """
    try:
        response = await groqChat.getPersonas(personaRequest)
        return response
    except Exception as e:
        warnings.warn(str(e))
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/chat/campaign", tags=["Chat"], response_model=CampaignAnalysisResponse)
async def campaign(campaignRequest: CampaignRequest = Body(None)):
    """
    Returns personas to the given attributes
    :param data:
    :return:
    """
    try:
        response = await groqChat.getCampaignAnalysis(campaignRequest)
        return response
    except Exception as e:
        warnings.warn(str(e))
        raise HTTPException(status_code=404, detail=str(e))
