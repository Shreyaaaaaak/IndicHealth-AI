from typing import Optional
from pydantic import BaseModel, Field


class ProfileCreate(BaseModel):
    age: Optional[int] = Field(None, ge=1, le=120, example=35)
    gender: Optional[str] = Field(None, example="Male")
    blood_group: Optional[str] = Field(None, example="O+")
    allergies: Optional[str] = Field(None, example="Penicillin, Dust")
    medical_history: Optional[str] = Field(None, example="Mild Asthma, Hypertension")


class ProfileUpdate(BaseModel):
    age: Optional[int] = Field(None, ge=1, le=120, example=36)
    gender: Optional[str] = Field(None, example="Male")
    blood_group: Optional[str] = Field(None, example="O+")
    allergies: Optional[str] = Field(None, example="Penicillin")
    medical_history: Optional[str] = Field(None, example="Hypertension")


class ProfileOut(BaseModel):
    id: int
    user_id: int
    age: Optional[int] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None

    class Config:
        from_attributes = True
