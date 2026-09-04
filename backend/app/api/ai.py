import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.database import get_db
from app.api.deps import get_current_user, owned_course
from app.models import User, Flashcard, Quiz, QuizQuestion, DocumentChunk
from app.schemas import ChatRequest, ChatResponse, GenerateRequest, GeneratedCount
from app.ai.rag import answer
from app.ai.providers import generation_provider
from app.ai.json_utils import parse_json_array

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    owned_course(payload.course_id, user, db)
    try:
        return answer(db, payload.course_id, payload.message, payload.provider)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))

def _context(db: Session, course_id: int) -> str:
    rows = db.scalars(
        select(DocumentChunk)
        .where(DocumentChunk.course_id == course_id)
        .order_by(DocumentChunk.material_id, DocumentChunk.chunk_index)
        .limit(12)
    ).all()
    return "\n\n".join(chunk.content for chunk in rows)

@router.post("/flashcards/generate", response_model=GeneratedCount)
def generate_flashcards(payload: GenerateRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    owned_course(payload.course_id, user, db)
    context = _context(db, payload.course_id)
    if not context.strip():
        raise HTTPException(status_code=409, detail="Upload and successfully process course material before generating flashcards")
    prompt = f"""Return ONLY valid JSON array with exactly {payload.count} objects:
[{{"question":"...", "answer":"..."}}]
Use only this course context:
{context}
"""
    try:
        raw = generation_provider().generate("You create concise educational flashcards and return strict JSON only.", prompt)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    try:
        data = parse_json_array(raw)
    except (json.JSONDecodeError, ValueError):
        raise HTTPException(status_code=502, detail="AI provider returned invalid JSON")
    created = 0
    for item in data[:payload.count]:
        if isinstance(item, dict) and item.get("question") and item.get("answer"):
            db.add(Flashcard(course_id=payload.course_id, user_id=user.id, question=str(item["question"]), answer=str(item["answer"])))
            created += 1
    if created == 0:
        db.rollback()
        raise HTTPException(status_code=502, detail="AI provider returned no valid flashcards")
    db.commit()
    return GeneratedCount(created=created)

@router.post("/quiz/generate", response_model=GeneratedCount)
def generate_quiz(payload: GenerateRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    owned_course(payload.course_id, user, db)
    context = _context(db, payload.course_id)
    if not context.strip():
        raise HTTPException(status_code=409, detail="Upload and successfully process course material before generating a quiz")
    prompt = f"""Return ONLY valid JSON array with exactly {payload.count} objects:
[{{"question":"...", "options":["A","B","C","D"], "correct_index":0, "explanation":"..."}}]
correct_index must be 0,1,2,or 3.
Use only this course context:
{context}
"""
    try:
        raw = generation_provider().generate("You create grounded educational multiple-choice quizzes and return strict JSON only.", prompt)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    try:
        data = parse_json_array(raw)
    except (json.JSONDecodeError, ValueError):
        raise HTTPException(status_code=502, detail="AI provider returned invalid JSON")
    valid_items = []
    for item in data[:payload.count]:
        if not isinstance(item, dict):
            continue
        options = item.get("options", [])
        correct_index = item.get("correct_index")
        if (
            item.get("question")
            and isinstance(options, list)
            and len(options) == 4
            and isinstance(correct_index, int)
            and 0 <= correct_index <= 3
        ):
            valid_items.append(item)
    if not valid_items:
        raise HTTPException(status_code=502, detail="AI provider returned no valid quiz questions")
    quiz = Quiz(course_id=payload.course_id, title="AI Generated Quiz")
    db.add(quiz); db.flush()
    for item in valid_items:
        options = item["options"]
        db.add(QuizQuestion(
            quiz_id=quiz.id,
            question=str(item["question"]),
            option_a=str(options[0]), option_b=str(options[1]), option_c=str(options[2]), option_d=str(options[3]),
            correct_index=int(item["correct_index"]),
            explanation=str(item.get("explanation", "")),
        ))
    db.commit()
    return GeneratedCount(created=len(valid_items))
