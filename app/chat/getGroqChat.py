import json
from app.model.CampaignAnalysisModel import CampaignAnalysisResponse
from app.model.CampaignRequestModel import CampaignRequest
from app.model.ChatMessageModel import ChatCompletionAssistantMessageParam, ChatCompletionContentPartImageParam, ChatCompletionContentPartTextParam, ChatCompletionMessageParam, ChatCompletionUserMessageParam, ChatMessage, ImageURL, ResponseFormat
from groq import AsyncGroq
from typing import List
from app.model.OutcomeResponseModel import OutcomeRequest, OutcomeResponse
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
                
        messages.append(assistantMessage)
        
        
        jsonVal = json.loads(assistantMessage.content)
        try:
            analysis = jsonVal["analysis"]
        except:
            analysis = jsonVal["Analysis"]
        return CampaignAnalysisResponse(messages=messages,analysis=analysis)
        
    async def getOutcomes(self, outcomeRequest:OutcomeRequest):
        # Create the Groq client
        client = AsyncGroq(api_key=self.GROQ_API_KEY)
        prompt = f"""Generate a predictive outcomes analysis for the generated synthetic data. Include sections that focus on the following key metrics:
Engagement Rate Prediction: Provide a description of audience engagement likelihood, with a percentage metric.
Goal Attainment: Outline the effectiveness for achieving campaign goals, particularly for registrations or conversions, with a percentage metric.
Platform Effectiveness: Analyze the platforms’ performance in driving results, with a percentage metric.
Positive Sentiment: Predict the audience’s emotional reaction to the campaign, including familiarity and humor, with a percentage metric.
Click-Through Rate (CTR): Show the likelihood of generating clicks, influenced by urgency and emotional triggers, with a percentage metric.

Display each metric in a visually appealing format, ensuring percentage metrics are clearly placed next to each prediction for clarity and ease of understanding.

Strictly provide the response in this JSON format only - 
{{"outcomes":[{{"name":"Engagement Rate Prediction","description":"","val":"Percentage"}},{{"name":"Goal Attainment","description":"","val":"Percentage"}},{{"name":"Platform Effectiveness","description":"","val":"Percentage"}},{{"name":"Positive Sentiment","description":"","val":"Percentage"}},{{"name":"Click-Through Rate (CTR)","description":"","val":"Percentage"}}]}}
Do not include any text other than the JSON.

"""

        textContent = ChatCompletionContentPartTextParam(type="text", text=prompt)
        
        message = ChatCompletionUserMessageParam(role="user", content=[textContent])
        outcomeRequest.messages.append(message)
        messages = outcomeRequest.messages
        responseFormat = ResponseFormat(type="json_object")
        
        
        chat_completion = await client.chat.completions.create(model=self.model,
                                  max_tokens=2500,
                                  messages=messages,
                                  response_format= responseFormat)
        
        assistantMessage = ChatCompletionAssistantMessageParam(role="assistant", content = chat_completion.choices[0].message.content)
        
        
        jsonVal = json.loads(assistantMessage.content)
        try:
            outcomes = jsonVal["outcomes"]
        except:
            outcomes = jsonVal["Outcomes"]
        return OutcomeResponse(outcomes=outcomes)