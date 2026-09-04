from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.database import get_db
from app.api.deps import get_current_user, owned_course
from app.models import User, Flashcard, Quiz, QuizQuestion, QuizAttempt, Badge, UserBadge
from app.schemas import (
    FlashcardOut, FlashcardReview, QuizOut, QuizQuestionOut, QuizSubmit, QuizResult,
    ProgressOut, BadgeOut
)
from app.services.gamification_service import record_learning, level_for_xp, level_progress

router = APIRouter(tags=["learning"])

@router.get("/courses/{course_id}/flashcards", response_model=list[FlashcardOut])
def flashcards(course_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    owned_course(course_id, user, db)
    now = datetime.now(timezone.utc)
    stmt = select(Flashcard).where(
        Flashcard.course_id == course_id,
        Flashcard.user_id == user.id,
        (Flashcard.next_review_at.is_(None)) | (Flashcard.next_review_at <= now),
    ).order_by(Flashcard.id)
    return db.scalars(stmt).all()

@router.post("/flashcards/{flashcard_id}/review", response_model=FlashcardOut)
def review_flashcard(flashcard_id: int, payload: FlashcardReview, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    card = db.get(Flashcard, flashcard_id)
    if not card or card.user_id != user.id:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    now = datetime.now(timezone.utc)
    if card.next_review_at is not None and card.next_review_at > now:
        return card
    if payload.known:
        card.box = min(card.box + 1, 5)
        days = [1, 2, 4, 8, 16][card.box - 1]
        record_learning(db, user, "flashcard_known", 5, card.course_id)
    else:
        card.box = 1
        days = 1
        record_learning(db, user, "flashcard_retry", 1, card.course_id)
    card.next_review_at = now + timedelta(days=days)
    db.commit(); db.refresh(card)
    return card

@router.get("/courses/{course_id}/quiz", response_model=QuizOut)
def get_quiz(course_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    owned_course(course_id, user, db)
    quiz = db.scalar(select(Quiz).where(Quiz.course_id == course_id).order_by(Quiz.id.desc()))
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    questions = db.scalars(select(QuizQuestion).where(QuizQuestion.quiz_id == quiz.id).order_by(QuizQuestion.id)).all()
    return QuizOut(
        id=quiz.id,
        title=quiz.title,
        questions=[QuizQuestionOut(id=q.id, question=q.question, options=[q.option_a, q.option_b, q.option_c, q.option_d]) for q in questions],
    )

@router.post("/quizzes/{quiz_id}/submit", response_model=QuizResult)
def submit_quiz(quiz_id: int, payload: QuizSubmit, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    quiz = db.get(Quiz, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    owned_course(quiz.course_id, user, db)
    questions = db.scalars(select(QuizQuestion).where(QuizQuestion.quiz_id == quiz.id)).all()
    score, explanations = 0, []
    for q in questions:
        selected = payload.answers.get(q.id)
        if selected == q.correct_index:
            score += 1
        explanations.append(q.explanation)
    total = len(questions)
    perfect = total > 0 and score == total
    prior_attempt = db.scalar(
        select(QuizAttempt.id).where(QuizAttempt.quiz_id == quiz.id, QuizAttempt.user_id == user.id).limit(1)
    )
    xp = 0 if prior_attempt else score * 10 + (20 if perfect else 0)
    db.add(QuizAttempt(quiz_id=quiz.id, user_id=user.id, score=score, total=total, xp_awarded=xp))
    record_learning(db, user, "quiz_completed", xp, quiz.course_id, perfect=perfect and prior_attempt is None)
    db.commit()
    return QuizResult(score=score, total=total, xp_awarded=xp, explanations=explanations)

@router.get("/progress", response_model=ProgressOut)
def progress(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.execute(
        select(Badge).join(UserBadge, UserBadge.badge_id == Badge.id).where(UserBadge.user_id == user.id)
    ).scalars().all()
    level = level_for_xp(user.xp)
    return ProgressOut(
        xp=user.xp,
        level=level,
        level_progress=level_progress(user.xp),
        streak=user.streak,
        next_level_xp=level * 100,
        badges=[BadgeOut(code=b.code, name=b.name, description=b.description, icon=b.icon) for b in rows],
    )
