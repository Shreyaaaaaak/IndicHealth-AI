from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ReminderCreate(BaseModel):
    medicine_name: str
    dosage: str                     # e.g., "1 tablet", "5ml"
    frequency: str                  # e.g., "Daily", "Twice a day", "After food"
    reminder_time: str              # e.g., "08:00 AM", "02:00 PM", "08:00 PM"
    is_active: Optional[bool] = True
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    notes: Optional[str] = None


class ReminderUpdate(BaseModel):
    medicine_name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    reminder_time: Optional[str] = None
    is_active: Optional[bool] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    notes: Optional[str] = None


class ReminderOut(BaseModel):
    id: int
    user_id: int
    medicine_name: str
    dosage: str
    frequency: str
    reminder_time: str
    is_active: bool
    start_date: Optional[str]
    end_date: Optional[str]
    notes: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
