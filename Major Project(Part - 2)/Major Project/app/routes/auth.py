from datetime import timedelta
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin, UserOut, Token
from app.auth.security import hash_password, verify_password
from app.auth.jwt import create_access_token, get_current_user
from app.utils.response import success_response, error_response

router = APIRouter(tags=["Authentication"])


@router.post("/register", summary="Register a new user")
@router.post("/auth/register", summary="Register a new user (alias)")
def register(user_in: UserRegister, db: Session = Depends(get_db)):

    """Registers a new user after checking for email duplication."""
    existing_user = db.query(User).filter(User.email == user_in.email.lower()).first()
    if existing_user:
        return error_response(message="A user with this email address already exists.", status_code=400)

    hashed_pwd = hash_password(user_in.password)
    new_user = User(
        name=user_in.name.strip(),
        email=user_in.email.lower().strip(),
        password=hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    user_out = UserOut.model_validate(new_user).model_dump(mode="json")
    return success_response(data=user_out, status_code=201)


@router.post("/login", summary="User login & JWT token issuance")
@router.post("/auth/login", summary="User login & JWT token issuance (alias)")
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    """Authenticates user credentials and issues a JWT Bearer access token."""
    user = db.query(User).filter(User.email == user_in.email.lower()).first()
    if not user or not verify_password(user_in.password, user.password):
        return error_response(message="Invalid email address or password.", status_code=401)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token_str = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )

    user_out = UserOut.model_validate(user).model_dump(mode="json")
    token_payload = {
        "access_token": token_str,
        "token_type": "bearer",
        "user": user_out
    }
    return success_response(data=token_payload)


@router.get("/me", summary="Get currently logged-in user profile")
@router.get("/auth/me", summary="Get currently logged-in user profile (alias)")
def get_me(current_user: User = Depends(get_current_user)):

    """Returns details of the currently authenticated user."""
    user_out = UserOut.model_validate(current_user).model_dump(mode="json")
    return success_response(data=user_out)
