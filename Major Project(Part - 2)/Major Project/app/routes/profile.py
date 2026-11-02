from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.profile import HealthProfile
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileOut
from app.auth.jwt import get_current_user
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/profile", tags=["Health Profile"])


@router.post("", summary="Create user health profile")
def create_profile(
    profile_in: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Creates a new health profile for the authenticated user."""
    existing_profile = db.query(HealthProfile).filter(HealthProfile.user_id == current_user.id).first()
    if existing_profile:
        return error_response(message="Health profile already exists. Use PUT /profile to update.", status_code=400)

    new_profile = HealthProfile(
        user_id=current_user.id,
        age=profile_in.age,
        gender=profile_in.gender,
        blood_group=profile_in.blood_group,
        allergies=profile_in.allergies,
        medical_history=profile_in.medical_history
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    profile_out = ProfileOut.model_validate(new_profile).model_dump(mode="json")
    return success_response(data=profile_out, status_code=201)


@router.get("", summary="Get user health profile")
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves the health profile of the authenticated user."""
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == current_user.id).first()
    if not profile:
        return error_response(message="Health profile not found. Please create a profile first.", status_code=404)

    profile_out = ProfileOut.model_validate(profile).model_dump(mode="json")
    return success_response(data=profile_out)


@router.put("", summary="Update user health profile")
def update_profile(
    profile_in: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Updates existing health profile fields for the authenticated user."""
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == current_user.id).first()

    # If profile does not exist, create it transparently
    if not profile:
        profile = HealthProfile(user_id=current_user.id)
        db.add(profile)

    if profile_in.age is not None:
        profile.age = profile_in.age
    if profile_in.gender is not None:
        profile.gender = profile_in.gender
    if profile_in.blood_group is not None:
        profile.blood_group = profile_in.blood_group
    if profile_in.allergies is not None:
        profile.allergies = profile_in.allergies
    if profile_in.medical_history is not None:
        profile.medical_history = profile_in.medical_history

    db.commit()
    db.refresh(profile)

    profile_out = ProfileOut.model_validate(profile).model_dump(mode="json")
    return success_response(data=profile_out)
