from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    medicine_name = Column(String(100), unique=True, index=True, nullable=False)
    uses = Column(Text, nullable=False)
    dosage = Column(Text, nullable=False)
    side_effects = Column(Text, nullable=False)
    precautions = Column(Text, nullable=False)
