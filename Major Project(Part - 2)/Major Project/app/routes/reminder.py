from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.reminder import MedicationReminder
from app.schemas.reminder import ReminderCreate, ReminderUpdate, ReminderOut
from app.auth.jwt import get_current_user
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/reminders", tags=["Medication & Pill Reminders"])


@router.post("", summary="Create a new medication reminder")
def create_reminder(
    reminder_in: ReminderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Adds a new daily dosage schedule for the authenticated patient."""
    new_reminder = MedicationReminder(
        user_id=current_user.id,
        medicine_name=reminder_in.medicine_name.strip(),
        dosage=reminder_in.dosage.strip(),
        frequency=reminder_in.frequency.strip(),
        reminder_time=reminder_in.reminder_time.strip(),
        is_active=reminder_in.is_active if reminder_in.is_active is not None else True,
        start_date=reminder_in.start_date,
        end_date=reminder_in.end_date,
        notes=reminder_in.notes
    )

    db.add(new_reminder)
    db.commit()
    db.refresh(new_reminder)

    reminder_out = ReminderOut.model_validate(new_reminder).model_dump(mode="json")
    return success_response(data=reminder_out, status_code=201)


@router.get("", summary="List all medication reminders for current user")
def list_reminders(
    active_only: Optional[bool] = Query(None, description="Filter for active reminders only"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(MedicationReminder).filter(MedicationReminder.user_id == current_user.id)
    if active_only is not None:
        query = query.filter(MedicationReminder.is_active == active_only)

    reminders = query.order_by(MedicationReminder.reminder_time.asc()).all()
    reminders_out = [ReminderOut.model_validate(r).model_dump(mode="json") for r in reminders]
    return success_response(data=reminders_out)


@router.get("/due", summary="Get reminders due or active for notification")
def get_due_reminders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Returns active reminders for the patient."""
    reminders = (
        db.query(MedicationReminder)
        .filter(MedicationReminder.user_id == current_user.id, MedicationReminder.is_active == True)
        .order_by(MedicationReminder.reminder_time.asc())
        .all()
    )
    reminders_out = [ReminderOut.model_validate(r).model_dump(mode="json") for r in reminders]
    return success_response(data=reminders_out)


@router.get("/{reminder_id}", summary="Get reminder details by ID")
def get_reminder(
    reminder_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    reminder = (
        db.query(MedicationReminder)
        .filter(MedicationReminder.id == reminder_id, MedicationReminder.user_id == current_user.id)
        .first()
    )
    if not reminder:
        return error_response(message="Reminder not found.", status_code=404)

    reminder_out = ReminderOut.model_validate(reminder).model_dump(mode="json")
    return success_response(data=reminder_out)


@router.put("/{reminder_id}", summary="Update or toggle a medication reminder")
def update_reminder(
    reminder_id: int,
    update_in: ReminderUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    reminder = (
        db.query(MedicationReminder)
        .filter(MedicationReminder.id == reminder_id, MedicationReminder.user_id == current_user.id)
        .first()
    )
    if not reminder:
        return error_response(message="Reminder not found.", status_code=404)

    if update_in.medicine_name is not None:
        reminder.medicine_name = update_in.medicine_name.strip()
    if update_in.dosage is not None:
        reminder.dosage = update_in.dosage.strip()
    if update_in.frequency is not None:
        reminder.frequency = update_in.frequency.strip()
    if update_in.reminder_time is not None:
        reminder.reminder_time = update_in.reminder_time.strip()
    if update_in.is_active is not None:
        reminder.is_active = update_in.is_active
    if update_in.start_date is not None:
        reminder.start_date = update_in.start_date
    if update_in.end_date is not None:
        reminder.end_date = update_in.end_date
    if update_in.notes is not None:
        reminder.notes = update_in.notes

    db.commit()
    db.refresh(reminder)

    reminder_out = ReminderOut.model_validate(reminder).model_dump(mode="json")
    return success_response(data=reminder_out)


@router.delete("/{reminder_id}", summary="Delete a medication reminder")
def delete_reminder(
    reminder_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    reminder = (
        db.query(MedicationReminder)
        .filter(MedicationReminder.id == reminder_id, MedicationReminder.user_id == current_user.id)
        .first()
    )
    if not reminder:
        return error_response(message="Reminder not found.", status_code=404)

    db.delete(reminder)
    db.commit()
    return success_response(data={"deleted_id": reminder_id})
