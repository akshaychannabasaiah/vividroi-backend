from app.model.ChatMessageModel import ChatMessage, ResponseFormat
from app.model.MessageModel import MessageContent, TextContent
from groq import AsyncGroq
from typing import List
from app.model.PersonaModel import Persona
from app.model.PersonaRequestModel import PersonaRequest
from pydantic import BaseModel, Field, Json
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
        prompt = f"""Create 10 personas for a marketing campaign with the following parameters: Age {req.age_min}-{req.age_max}, Gender {req.gender}, Location {req.location}, Other factors {req.other}.
                      Return a JSON of the 10 personas with the following fields :  name, age, gender, location, income_level, occupation, lifestyle_interests, ocean_trait, implicit_drivers, purchase_behaviors, and preferred_buying_platform."""
        textContent = TextContent(type="text", text=prompt)
        message = MessageContent(role="user", content=[textContent])
        messages = [message]
        responseFormat = ResponseFormat(type="json_object")
        chatMessage = ChatMessage(model=self.model,
                                  max_tokens=2500,
                                  messages=messages,
                                  response_format= responseFormat)
        
        chat_completion = await client.chat.completions.create(model=self.model,
                                  max_tokens=2500,
                                  messages=messages,
                                  response_format= responseFormat)
        return chat_completion.choices[0].message.content