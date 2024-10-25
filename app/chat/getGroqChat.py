from app.model.ChatMessageModel import ChatMessage
from app.model.MessageModel import MessageContent, TextContent
from groq import AsyncGroq
from typing import List
from app.model.PersonaModel import Persona
from app.model.PersonaRequestModel import PersonaRequest

from app.configuration.getConfig import Config
from app.helper.pattern.singleton import Singleton


class GroqChat(metaclass=Singleton):
    """
    Make connections to the groq api client
    """
    def __init__(self) -> None:
        
        # get the config file
        configuration = Config()
        self.GROQ_API_KEY = configuration.GROQ_API_KEY
        self.model = "llama-3.2-90b-vision-preview"
    
    async def getPersonas(self, req:PersonaRequest):
        # Create the Groq client
        client = AsyncGroq(api_key=self.GROQ_API_KEY)
        propmt = f"""Create 10 personas for a marketing campaign with the following parameters: Age {req.age_min}-{req.age_max}, Gender {req.gender}, Location {req.location}, Other factors {req.other}.
                      Return a JSON of the 10 personas with the following fields :  name, age, gender, location, income_level, occupation, lifestyle_interests, ocean_trait, implicit_drivers, purchase_behaviors, and preferred_buying_platform."""
        chatMessage = ChatMessage()
        chatMessage.model = self.model
        message = MessageContent()
        message.role = "user"
        message.content = TextContent()
        message.content.type = "text"
        message.content.text = propmt
        chatMessage.messages = MessageContent()[message]
        chatMessage.max_tokens = 2500
        chatMessage.response_format= """{"type": "json_object"}"""
        response = await client.chat.completions.create(chatMessage)
        return response