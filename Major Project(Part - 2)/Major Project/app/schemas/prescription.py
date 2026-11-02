from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class ExtractedMedicine(BaseModel):
    medicine_name: str
    strength: Optional[str] = "Not specified"
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None
    timing: Optional[str] = None
    instructions: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PrescriptionScanData(BaseModel):
    extracted_medicines: List[ExtractedMedicine]
    doctor_notes: Optional[str] = None
    confidence_score: Optional[str] = "High"

    model_config = ConfigDict(from_attributes=True)
