import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.database import engine, Base, SessionLocal
from app.services.seeder import seed_medicines
from app.services.doctor_seeder import seed_doctors
from app.services.facility_seeder import seed_facilities
from app.utils.response import error_response, success_response

# Import routers
from app.routes.auth import router as auth_router
from app.routes.profile import router as profile_router
from app.routes.chat import router as chat_router
from app.routes.symptom import router as symptom_router
from app.routes.medicine import router as medicine_router
from app.routes.appointment import router as appointment_router
from app.routes.prescription import router as prescription_router
from app.routes.reminder import router as reminder_router
from app.routes.facility import router as facility_router


# Initialize FastAPI App
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend APIs for AarogyaMitra: AI-Powered Multilingual Rural Healthcare Assistant",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Startup Event: Create DB tables, seed medicines, doctors, and facilities
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_medicines(db)
        seed_doctors(db)
        seed_facilities(db)
    finally:
        db.close()

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list + ["*"],  # Fallback wildcard for local dev flexibility
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Custom Exception Handlers for Standardized Response Format
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    msg = errors[0].get("msg") if errors else "Invalid request data format."
    loc = errors[0].get("loc") if errors else []
    field_name = loc[-1] if loc else "field"
    return error_response(message=f"Validation error on '{field_name}': {msg}", status_code=422)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return error_response(message=exc.detail, status_code=exc.status_code)


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return error_response(message=f"An unexpected internal error occurred: {str(exc)}", status_code=500)


# API Health Status Endpoint
@app.get("/health-status", summary="Backend Health Check Endpoint")
def health_status():
    return success_response(data={
        "status": "online",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs"
    })

# Mount Routers under API Version Prefix (/api)
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(profile_router, prefix=settings.API_V1_STR)
app.include_router(chat_router, prefix=settings.API_V1_STR)
app.include_router(symptom_router, prefix=settings.API_V1_STR)
app.include_router(medicine_router, prefix=settings.API_V1_STR)
app.include_router(appointment_router, prefix=settings.API_V1_STR)
app.include_router(prescription_router, prefix=settings.API_V1_STR)
app.include_router(reminder_router, prefix=settings.API_V1_STR)
app.include_router(facility_router, prefix=settings.API_V1_STR)

# Also mount routers at root level to match exact SRS specification paths (/register, /login, /me, /profile, /chat, etc.)
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(chat_router)
app.include_router(symptom_router)
app.include_router(medicine_router)
app.include_router(appointment_router)
app.include_router(prescription_router)
app.include_router(reminder_router)
app.include_router(facility_router)




# Serve Frontend Static UI Files at / if public folder exists
public_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "public")
if os.path.exists(public_dir):
    app.mount("/", StaticFiles(directory=public_dir, html=True), name="static")
