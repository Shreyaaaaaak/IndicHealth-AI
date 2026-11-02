from pydantic import BaseModel


class MedicineOut(BaseModel):
    id: int
    medicine_name: str
    uses: str
    dosage: str
    side_effects: str
    precautions: str

    class Config:
        from_attributes = True
