import json
from typing import List
import warnings
from app.chat.getGroqChat import GroqChat
from app.model.PersonaModel import Persona
from app.model.PersonaRequestModel import PersonaRequest
from fastapi import Depends, APIRouter, Body, HTTPException # type: ignore
from fastapi import BackgroundTasks # type: ignore
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

@router.post("/chat/personas", tags=["Persona,PersonaRequest"], response_model=List[Persona])
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


