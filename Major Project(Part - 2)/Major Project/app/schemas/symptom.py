from typing import List
from pydantic import BaseModel, Field


class SymptomCheckRequest(BaseModel):
    symptoms: List[str] = Field(..., min_items=1, example=["Fever", "Cough", "Headache"])


class SymptomCheckResponse(BaseModel):
    matched_symptoms: List[str]
    possible_condition: str
    recommended_specialist: str
    advice: str
    is_emergency: bool = False
