from fastapi import APIRouter
from app.schemas.symptom import SymptomCheckRequest
from app.services.symptom_service import check_symptoms
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/symptom-check", tags=["Symptom Checker"])


@router.post("", summary="Rule-based symptom assessment")
def symptom_check(payload: SymptomCheckRequest):
    """
    Evaluates list of symptoms against rule-based clinical logic.
    Returns condition assessment, specialist recommendation, advice, and emergency flags.
    """
    if not payload.symptoms:
        return error_response(message="Please provide at least one symptom to evaluate.", status_code=400)

    result = check_symptoms(payload.symptoms)
    return success_response(data=result)
