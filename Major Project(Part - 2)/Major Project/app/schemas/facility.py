from typing import Optional
from pydantic import BaseModel, ConfigDict


class FacilityOut(BaseModel):
    id: int
    name: str
    facility_type: str
    address: str
    district: str
    state: str
    contact_number: str
    latitude: float
    longitude: float
    emergency_24x7: bool
    operating_hours: str
    distance_km: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)
