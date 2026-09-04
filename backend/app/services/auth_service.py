from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from app.models import User, RefreshToken
from app.core.security import (
    hash_password, verify_password, create_access_token,
    create_refresh_token_value, hash_refresh_token, refresh_expiry, DUMMY_HASH
)

def _pair(db: Session, user: User):
    raw = create_refresh_token_value()
    db.add(RefreshToken(
        user_id=user.id,
        token_hash=hash_refresh_token(raw),
        expires_at=refresh_expiry(),
    ))
    db.commit()
    return create_access_token(user.id), raw

def register(db: Session, name: str, email: str, password: str):
    if db.scalar(select(User).where(User.email == email.lower())):
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(name=name.strip(), email=email.lower(), password_hash=hash_password(password))
    db.add(user); db.commit(); db.refresh(user)
    access, refresh = _pair(db, user)
    return user, access, refresh

def login(db: Session, email: str, password: str):
    user = db.scalar(select(User).where(User.email == email.lower()))
    if not user:
        verify_password(password, DUMMY_HASH)
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access, refresh = _pair(db, user)
    return user, access, refresh

def rotate_refresh(db: Session, raw_token: str):
    token_hash = hash_refresh_token(raw_token)
    row = db.scalar(
        select(RefreshToken)
        .where(RefreshToken.token_hash == token_hash)
        .with_for_update()
    )
    now = datetime.now(timezone.utc)
    if not row or row.revoked_at is not None or row.expires_at <= now:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    row.revoked_at = now
    user = db.get(User, row.user_id)
    new_access, new_refresh = _pair(db, user)
    return new_access, new_refresh

def revoke_refresh(db: Session, raw_token: str):
    row = db.scalar(select(RefreshToken).where(RefreshToken.token_hash == hash_refresh_token(raw_token)))
    if row and row.revoked_at is None:
        row.revoked_at = datetime.now(timezone.utc)
        db.commit()
