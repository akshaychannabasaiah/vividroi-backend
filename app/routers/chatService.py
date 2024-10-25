import json
from typing import List
from app.chat.getGroqChat import GroqChat
from app.model.PersonaModel import Persona
from app.model.PersonaRequestModel import PersonaRequest
from fastapi import Depends, APIRouter, Body
from fastapi import BackgroundTasks
from app.configuration.getConfig import Config
import groq


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
    response = await groqChat.getPersonas(personaRequest)
    return response


