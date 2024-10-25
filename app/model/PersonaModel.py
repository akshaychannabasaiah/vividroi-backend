from typing import List
from pydantic import BaseModel

class Persona(BaseModel):
    name: str
    age: int
    gender: str
    location: str
    income_level: str
    occupation: str
    lifestyle_interests: List[str]
    ocean_trait: str
    implicit_drivers: List[str]
    purchase_behaviours: List[str]
    prefered_buying_platform: str