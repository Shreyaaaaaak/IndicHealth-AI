from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    specialty = Column(String(100), index=True, nullable=False)
    qualification = Column(String(100), nullable=False)
    experience_years = Column(Integer, default=5, nullable=False)
    hospital_name = Column(String(200), nullable=False)
    location = Column(String(100), nullable=False)
    contact_phone = Column(String(20), nullable=False)
    consultation_fee = Column(Integer, default=0, nullable=False)  # 0 for PHC / Govt centers
    available_days = Column(String(100), default="Mon,Tue,Wed,Thu,Fri", nullable=False)
    available_time = Column(String(100), default="09:00 AM - 01:00 PM, 05:00 PM - 08:00 PM", nullable=False)

    # Relationships
    appointments = relationship("Appointment", back_populates="doctor", cascade="all, delete-orphan")
