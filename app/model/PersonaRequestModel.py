from pydantic import BaseModel

class PersonaRequest(BaseModel):
    age_min: int
    age_max: int
    gender: str
    location: str
    other: str