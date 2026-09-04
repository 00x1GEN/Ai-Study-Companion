from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import RegisterRequest, LoginRequest, RefreshRequest, TokenPair, UserOut, Message
from app.services import auth_service
from app.api.deps import get_current_user
from app.models import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenPair, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    _, access, refresh = auth_service.register(db, payload.name, payload.email, payload.password)
    return TokenPair(access_token=access, refresh_token=refresh)

@router.post("/login", response_model=TokenPair)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    _, access, refresh = auth_service.login(db, payload.email, payload.password)
    return TokenPair(access_token=access, refresh_token=refresh)

@router.post("/refresh", response_model=TokenPair)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    access, refresh_token = auth_service.rotate_refresh(db, payload.refresh_token)
    return TokenPair(access_token=access, refresh_token=refresh_token)

@router.post("/logout", response_model=Message)
def logout(payload: RefreshRequest, db: Session = Depends(get_db)):
    auth_service.revoke_refresh(db, payload.refresh_token)
    return Message(message="Logged out")

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
