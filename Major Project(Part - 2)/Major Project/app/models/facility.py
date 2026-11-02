from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base


class HealthcareFacility(Base):
    __tablename__ = "healthcare_facilities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    facility_type = Column(String(50), index=True, nullable=False)  # PHC, CHC, Hospital, Pharmacy
    address = Column(String(255), nullable=False)
    district = Column(String(100), index=True, nullable=False)
    state = Column(String(100), default="West Bengal", nullable=False)
    contact_number = Column(String(25), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    emergency_24x7 = Column(Boolean, default=False, nullable=False)
    operating_hours = Column(String(100), default="Open 24 Hours", nullable=False)
