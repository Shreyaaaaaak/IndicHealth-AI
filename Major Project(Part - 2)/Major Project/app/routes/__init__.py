from app.routes.auth import router as auth_router
from app.routes.profile import router as profile_router
from app.routes.chat import router as chat_router
from app.routes.symptom import router as symptom_router
from app.routes.medicine import router as medicine_router
from app.routes.appointment import router as appointment_router
from app.routes.prescription import router as prescription_router
from app.routes.reminder import router as reminder_router
from app.routes.facility import router as facility_router

__all__ = [
    "auth_router",
    "profile_router",
    "chat_router",
    "symptom_router",
    "medicine_router",
    "appointment_router",
    "prescription_router",
    "reminder_router",
    "facility_router"
]



