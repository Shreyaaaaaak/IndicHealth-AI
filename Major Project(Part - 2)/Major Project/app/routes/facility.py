from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.facility import HealthcareFacility
from app.schemas.facility import FacilityOut
from app.services.geo_service import haversine_distance
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/facilities", tags=["Nearby Healthcare Facilities & PHCs"])


@router.get("/nearby", summary="Find healthcare facilities near given GPS coordinates")
def get_nearby_facilities(
    lat: float = Query(..., description="User latitude (e.g. 22.72)"),
    lng: float = Query(..., description="User longitude (e.g. 88.48)"),
    radius_km: float = Query(15.0, description="Search radius in kilometers (default: 15km)"),
    facility_type: Optional[str] = Query(None, description="Filter by type (PHC, CHC, Hospital, Pharmacy)"),
    emergency_only: bool = Query(False, description="Filter for 24x7 emergency facilities only"),
    db: Session = Depends(get_db)
):
    """
    Computes exact straight-line distances using the Haversine formula,
    filters facilities within radius_km, and sorts them from closest to farthest.
    """
    query = db.query(HealthcareFacility)

    if facility_type:
        query = query.filter(HealthcareFacility.facility_type.ilike(f"%{facility_type.strip()}%"))

    if emergency_only:
        query = query.filter(HealthcareFacility.emergency_24x7 == True)

    all_facilities = query.all()
    results = []

    for fac in all_facilities:
        dist = haversine_distance(lat, lng, fac.latitude, fac.longitude)
        if dist <= radius_km:
            fac_dict = FacilityOut.model_validate(fac).model_dump(mode="json")
            fac_dict["distance_km"] = dist
            results.append(fac_dict)

    # Sort results by closest distance first
    results.sort(key=lambda x: x["distance_km"])
    return success_response(data=results)


@router.get("/search", summary="Search healthcare facilities by district, name, or type")
def search_facilities(
    district: Optional[str] = Query(None, description="District name (e.g. North 24 Parganas, Kolkata)"),
    facility_type: Optional[str] = Query(None, description="Facility type (PHC, CHC, Hospital, Pharmacy)"),
    query_str: Optional[str] = Query(None, description="Search keyword for name or address"),
    db: Session = Depends(get_db)
):
    query = db.query(HealthcareFacility)

    if district:
        query = query.filter(HealthcareFacility.district.ilike(f"%{district.strip()}%"))

    if facility_type:
        query = query.filter(HealthcareFacility.facility_type.ilike(f"%{facility_type.strip()}%"))

    if query_str:
        term = f"%{query_str.strip()}%"
        query = query.filter(
            (HealthcareFacility.name.ilike(term)) |
            (HealthcareFacility.address.ilike(term))
        )

    facilities = query.all()
    results = [FacilityOut.model_validate(f).model_dump(mode="json") for f in facilities]
    return success_response(data=results)


@router.get("/{facility_id}", summary="Get healthcare facility details by ID")
def get_facility(facility_id: int, db: Session = Depends(get_db)):
    facility = db.query(HealthcareFacility).filter(HealthcareFacility.id == facility_id).first()
    if not facility:
        return error_response(message="Facility not found.", status_code=404)

    fac_out = FacilityOut.model_validate(facility).model_dump(mode="json")
    return success_response(data=fac_out)
