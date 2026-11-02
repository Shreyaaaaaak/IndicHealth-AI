from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.medicine import Medicine
from app.schemas.medicine import MedicineOut
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/medicine", tags=["Medicine Information"])


@router.get("/{medicine_name}", summary="Search medicine details by name")
def get_medicine_by_name(medicine_name: str, db: Session = Depends(get_db)):
    """
    Searches for medicine information by name (case-insensitive).
    Returns Uses, Dosage, Side Effects, and Precautions.
    """
    clean_name = medicine_name.strip()
    if not clean_name:
        return error_response(message="Medicine name search parameter cannot be empty.", status_code=400)

    # Perform case-insensitive search using LOWER()
    medicine = db.query(Medicine).filter(func.lower(Medicine.medicine_name) == clean_name.lower()).first()

    # Fallback to partial match if exact match not found
    if not medicine:
        medicine = db.query(Medicine).filter(func.lower(Medicine.medicine_name).contains(clean_name.lower())).first()

    if not medicine:
        return error_response(
            message=f"Medicine '{medicine_name}' not found in database. Please check spelling or consult a pharmacist.",
            status_code=404
        )

    med_out = MedicineOut.model_validate(medicine).model_dump(mode="json")
    return success_response(data=med_out)


@router.get("", summary="List all seeded medicines")
@router.get("s", summary="List all seeded medicines (alias)")
def list_medicines(db: Session = Depends(get_db)):
    """Retrieves all medicines available in the database."""
    medicines = db.query(Medicine).order_by(Medicine.medicine_name.asc()).all()
    meds_out = [MedicineOut.model_validate(m).model_dump(mode="json") for m in medicines]
    return success_response(data=meds_out)
