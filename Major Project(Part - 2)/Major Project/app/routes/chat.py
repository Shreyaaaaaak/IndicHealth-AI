from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.profile import HealthProfile
from app.models.chat import ChatHistory
from app.schemas.chat import ChatRequest, ChatResponse, ChatHistoryOut
from app.auth.jwt import get_current_user, get_optional_current_user
from app.services.ai_service import generate_ai_response
from app.utils.response import success_response

router = APIRouter(prefix="/chat", tags=["AI Chat Assistant"])


@router.post("", summary="Chat with AarogyaMitra AI Assistant")
@router.post("/chat", summary="Chat with AarogyaMitra AI Assistant (alias)")
async def chat_with_ai(
    chat_in: ChatRequest,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Processes user query using Gemini AI.
    Works for both logged-in users (attaches profile context & saves history)
    and Guest users (provides AI guidance directly without requiring authentication).
    """
    # Fetch patient profile summary if user is logged in
    profile_summary = ""
    if current_user:
        profile = db.query(HealthProfile).filter(HealthProfile.user_id == current_user.id).first()
        if profile:
            profile_summary = (
                f"Age: {profile.age or 'N/A'}, Gender: {profile.gender or 'N/A'}, "
                f"Allergies: {profile.allergies or 'None'}, Medical History: {profile.medical_history or 'None'}"
            )

    # Generate AI Response
    ai_text = await generate_ai_response(
        user_message=chat_in.message,
        health_profile_summary=profile_summary
    )

    # Save to ChatHistory database if user is logged in
    if current_user:
        chat_entry = ChatHistory(
            user_id=current_user.id,
            user_message=chat_in.message,
            ai_response=ai_text
        )
        db.add(chat_entry)
        db.commit()

    return success_response(data={"response": ai_text})


@router.get("/history", summary="Get user's past AI chat history")
@router.get("/chat/history", summary="Get user's past AI chat history (alias)")
def get_chat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves all past AI chat logs for the current authenticated user."""
    history = db.query(ChatHistory).filter(ChatHistory.user_id == current_user.id).order_by(ChatHistory.timestamp.asc()).all()
    history_out = [ChatHistoryOut.model_validate(h).model_dump(mode="json") for h in history]
    return success_response(data=history_out)
