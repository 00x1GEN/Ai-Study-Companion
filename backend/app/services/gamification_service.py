from datetime import date, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import User, Badge, UserBadge, LearningEvent

BADGES = [
    ("FIRST_STEP", "First Step", "Complete your first learning activity.", "flag"),
    ("STREAK_3", "Three-Day Streak", "Study on three consecutive days.", "local_fire_department"),
    ("XP_500", "500 XP", "Earn 500 experience points.", "stars"),
    ("QUIZ_MASTER", "Quiz Master", "Complete a quiz with a perfect score.", "emoji_events"),
]

def seed_badges(db: Session):
    existing = {x.code for x in db.scalars(select(Badge)).all()}
    for code, name, desc, icon in BADGES:
        if code not in existing:
            db.add(Badge(code=code, name=name, description=desc, icon=icon))
    db.commit()

def _award_badge(db: Session, user: User, code: str):
    badge = db.scalar(select(Badge).where(Badge.code == code))
    if not badge:
        return
    exists = db.get(UserBadge, {"user_id": user.id, "badge_id": badge.id})
    if not exists:
        db.add(UserBadge(user_id=user.id, badge_id=badge.id))

def record_learning(db: Session, user: User, kind: str, xp: int, course_id: int | None = None, perfect: bool = False):
    today = date.today()
    if user.last_learning_date is None:
        user.streak = 1
    elif user.last_learning_date == today:
        pass
    elif user.last_learning_date == today - timedelta(days=1):
        user.streak += 1
    else:
        user.streak = 1
    user.last_learning_date = today
    user.xp += xp
    db.add(LearningEvent(user_id=user.id, course_id=course_id, kind=kind, xp=xp))
    _award_badge(db, user, "FIRST_STEP")
    if user.streak >= 3:
        _award_badge(db, user, "STREAK_3")
    if user.xp >= 500:
        _award_badge(db, user, "XP_500")
    if perfect:
        _award_badge(db, user, "QUIZ_MASTER")
    db.flush()

def level_for_xp(xp: int) -> int:
    return xp // 100 + 1

def level_progress(xp: int) -> float:
    return (xp % 100) / 100.0
