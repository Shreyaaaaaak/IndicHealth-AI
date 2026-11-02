from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class MedicationReminder(Base):
    __tablename__ = "medication_reminders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    medicine_name = Column(String(150), nullable=False)
    dosage = Column(String(100), nullable=False)            # e.g., "1 tablet", "5ml"
    frequency = Column(String(100), nullable=False)         # e.g., "Daily", "Twice a day", "After food"
    reminder_time = Column(String(50), nullable=False)      # e.g., "08:00 AM", "02:00 PM", "08:00 PM"
    is_active = Column(Boolean, default=True, nullable=False)
    start_date = Column(String(20), nullable=True)          # YYYY-MM-DD
    end_date = Column(String(20), nullable=True)            # YYYY-MM-DD
    notes = Column(Text, nullable=True)                     # e.g., "Take with warm water"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship to user
    user = relationship("User", back_populates="reminders")
