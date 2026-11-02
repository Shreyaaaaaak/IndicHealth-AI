from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class DoctorOut(BaseModel):
    id: int
    name: str
    specialty: str
    qualification: str
    experience_years: int
    hospital_name: str
    location: str
    contact_phone: str
    consultation_fee: int
    available_days: str
    available_time: str

    model_config = ConfigDict(from_attributes=True)


class AppointmentCreate(BaseModel):
    doctor_id: int
    appointment_date: str  # YYYY-MM-DD
    time_slot: str        # e.g., "10:30 AM"
    patient_name: str
    patient_phone: str
    symptoms_summary: Optional[str] = None


class AppointmentUpdateStatus(BaseModel):
    status: str  # pending, confirmed, completed, cancelled


class AppointmentOut(BaseModel):
    id: int
    user_id: int
    doctor_id: int
    doctor: DoctorOut
    patient_name: str
    patient_phone: str
    appointment_date: str
    time_slot: str
    symptoms_summary: Optional[str]
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
