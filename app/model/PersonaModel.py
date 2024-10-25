from typing import List
from pydantic import BaseModel

class Persona(BaseModel):
    name: str
    age: int
    gender: str
    location: str
    income_level: str
    occupation: str
    lifestyle_interests: str
    ocean_trait: str
    implicit_drivers: str
    purchase_behaviors: str
    preferred_buying_platform: str