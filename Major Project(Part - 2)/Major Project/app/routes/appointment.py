from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.user import User
from app.models.doctor import Doctor
from app.models.appointment import Appointment
from app.schemas.appointment import DoctorOut, AppointmentCreate, AppointmentOut, AppointmentUpdateStatus
from app.auth.jwt import get_current_user
from app.utils.response import success_response, error_response

router = APIRouter(tags=["Doctor Directory & Appointments"])


# -------------------------------------------------------------
# 1. Doctor Directory Endpoints
# -------------------------------------------------------------
@router.get("/doctors", summary="List all verified doctors with optional specialty and search filters")
def list_doctors(
    specialty: Optional[str] = Query(None, description="Filter by specialty (e.g. Cardiologist, General Physician)"),
    search: Optional[str] = Query(None, description="Search by doctor name or hospital name"),
    db: Session = Depends(get_db)
):
    query = db.query(Doctor)

    if specialty:
        query = query.filter(Doctor.specialty.ilike(f"%{specialty.strip()}%"))

    if search:
        search_term = f"%{search.strip()}%"
        query = query.filter(
            (Doctor.name.ilike(search_term)) |
            (Doctor.hospital_name.ilike(search_term)) |
            (Doctor.location.ilike(search_term))
        )

    doctors = query.all()
    doctors_out = [DoctorOut.model_validate(d).model_dump(mode="json") for d in doctors]
    return success_response(data=doctors_out)


@router.get("/doctors/{doctor_id}", summary="Get doctor details by ID")
def get_doctor_by_id(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        return error_response(message="Doctor not found.", status_code=404)
    doctor_out = DoctorOut.model_validate(doctor).model_dump(mode="json")
    return success_response(data=doctor_out)


# -------------------------------------------------------------
# 2. Appointment Booking Endpoints
# -------------------------------------------------------------
@router.post("/appointments", summary="Book an appointment with a doctor")
def book_appointment(
    appt_in: AppointmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == appt_in.doctor_id).first()
    if not doctor:
        return error_response(message="Doctor not found. Please choose an existing doctor.", status_code=404)

    # Patient name fallback if blank
    patient_name = appt_in.patient_name.strip() if appt_in.patient_name else (current_user.name or "Patient")
    patient_phone = appt_in.patient_phone.strip() if appt_in.patient_phone else "N/A"

    new_appt = Appointment(
        user_id=current_user.id,
        doctor_id=appt_in.doctor_id,
        patient_name=patient_name,
        patient_phone=patient_phone,
        appointment_date=appt_in.appointment_date,
        time_slot=appt_in.time_slot,
        symptoms_summary=appt_in.symptoms_summary,
        status="confirmed"
    )

    db.add(new_appt)
    db.commit()
    db.refresh(new_appt)

    # Load with doctor relationship for complete response
    appt_with_doc = db.query(Appointment).options(joinedload(Appointment.doctor)).filter(Appointment.id == new_appt.id).first()
    appt_out = AppointmentOut.model_validate(appt_with_doc).model_dump(mode="json")
    return success_response(data=appt_out, status_code=201)


@router.get("/appointments", summary="List all appointments for the current authenticated user")
def list_user_appointments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    appointments = (
        db.query(Appointment)
        .options(joinedload(Appointment.doctor))
        .filter(Appointment.user_id == current_user.id)
        .order_by(Appointment.created_at.desc())
        .all()
    )
    appointments_out = [AppointmentOut.model_validate(a).model_dump(mode="json") for a in appointments]
    return success_response(data=appointments_out)


@router.get("/appointments/{appointment_id}", summary="Get appointment details by ID")
def get_appointment_details(
    appointment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    appointment = (
        db.query(Appointment)
        .options(joinedload(Appointment.doctor))
        .filter(Appointment.id == appointment_id, Appointment.user_id == current_user.id)
        .first()
    )
    if not appointment:
        return error_response(message="Appointment not found or unauthorized.", status_code=404)

    appt_out = AppointmentOut.model_validate(appointment).model_dump(mode="json")
    return success_response(data=appt_out)


@router.put("/appointments/{appointment_id}/cancel", summary="Cancel an appointment")
def cancel_appointment(
    appointment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    appointment = (
        db.query(Appointment)
        .options(joinedload(Appointment.doctor))
        .filter(Appointment.id == appointment_id, Appointment.user_id == current_user.id)
        .first()
    )
    if not appointment:
        return error_response(message="Appointment not found or unauthorized.", status_code=404)

    if appointment.status == "cancelled":
        return error_response(message="Appointment is already cancelled.", status_code=400)

    appointment.status = "cancelled"
    db.commit()
    db.refresh(appointment)

    appt_out = AppointmentOut.model_validate(appointment).model_dump(mode="json")
    return success_response(data=appt_out)
