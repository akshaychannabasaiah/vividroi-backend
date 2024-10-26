import json
from app.model.CampaignAnalysisModel import CampaignAnalysisResponse
from app.model.CampaignRequestModel import CampaignRequest
from app.model.ChatMessageModel import ChatCompletionAssistantMessageParam, ChatCompletionContentPartImageParam, ChatCompletionContentPartTextParam, ChatCompletionMessageParam, ChatCompletionUserMessageParam, ChatMessage, ImageURL, ResponseFormat
from groq import AsyncGroq
from typing import List
from app.model.PersonaModel import Persona, PersonaResponse
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
                     Return a JSON of the 10 personas with the following fields :  name, age, gender, location, income_level, occupation, lifestyle_interests, ocean_trait, implicit_drivers, purchase_behaviors, and preferred_buying_platform.                      
                     Strictly adhere to this JSON format {{"personas":[{{"name":"","age":"","gender":"","location":"","income_level":"","occupation":"","lifestyle_interests":" ","ocean_trait":"","implicit_drivers":" ","purchase_behaviors":" ","preferred_buying_platform":""}}]}}"""
        textContent = ChatCompletionContentPartTextParam(type="text", text=prompt)
        message = ChatCompletionUserMessageParam(role="user", content=[textContent])
        messages = [message]
        responseFormat = ResponseFormat(type="json_object")
        
        chat_completion = await client.chat.completions.create(model=self.model,
                                  max_tokens=2500,
                                  messages=messages,
                                  response_format= responseFormat)
        
        assistantMessage = ChatCompletionAssistantMessageParam(role="assistant", content = chat_completion.choices[0].message.content)
        
        messages.append(assistantMessage)
        
        
        jsonVal = json.loads(assistantMessage.content)
        try:
            personas = jsonVal["personas"]
        except:
            personas = jsonVal["Personas"]
        return PersonaResponse(messages=messages,personas=personas)
         
    
    async def getCampaignAnalysis(self, req:CampaignRequest):
        # Create the Groq client
        client = AsyncGroq(api_key=self.GROQ_API_KEY)
        prompt = f"""Generate a campaign analysis based on the uploaded campaign data. Name of the campaign: {req.name}, Objective of the campign: {req.objective}. The analysis should include three sections based on the synthetic data: Platform Selection, Implicit Drivers, OCEAN Personality Traits. For each section, provide comparison data that can be put into a chart (Each section vs count), corresponding observations that explain the insights from the data and recommendations that suggest how to optimize the campaign based on these findings.
Strictly provide the response in this JSON format only {{"analysis":[{{"name":"Platform Selection","table":{{"xlabel":"Platform","ylabel":"Count","values":{{"Platform1":"count","Platform2":"count"}}}},"observation":"","recommendation":""}},{{"name":"Implicit Drivers","table":{{"xlabel":"Implicit Driver","ylabel":"Count","values":{{"Implicit Driver 1":"count","Implicit Driver 2":"count"}}}},"observation":"","recommendation":""}},{{"name":"OCEAN Personality Traits","table":{{"xlabel":"OCEAN Trait","ylabel":"Count","values":{{"OCEAN Trait 1":"count","OCEAN Trait 1":"count"}}}},"observation":"","recommendation":""}}]}}
Do not include any text other than the JSON.
"""

        # textContent = TextContent(type="text", text=prompt)
        # imageContent = ImageContent(type="image_url",image_url=ImageUrl(url=req.img))
        # message = MessageContent(role="user", content=[textContent, imageContent])
        # messages = req.messages.append(message)
        # messages = req.messages

        textContent = ChatCompletionContentPartTextParam(type="text", text=prompt)
        imageContent = ChatCompletionContentPartImageParam(type="image_url", image_url=ImageURL(url=req.img))
        
        message = ChatCompletionUserMessageParam(role="user", content=[textContent, imageContent])
        req.messages.append(message)
        messages = req.messages
        responseFormat = ResponseFormat(type="json_object")
        
        
        chat_completion = await client.chat.completions.create(model=self.model,
                                  max_tokens=2500,
                                  messages=messages,
                                  response_format= responseFormat)
        
        assistantMessage = ChatCompletionAssistantMessageParam(role="assistant", content = chat_completion.choices[0].message.content)
        
        
        jsonVal = json.loads(assistantMessage.content)
        try:
            analysis = jsonVal["analysis"]
        except:
            analysis = jsonVal["Analysis"]
        return CampaignAnalysisResponse(messages=messages,analysis=analysis)