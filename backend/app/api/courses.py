from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.database import get_db
from app.core.config import settings
from app.api.deps import get_current_user, owned_course
from app.models import User, Course, Material
from app.schemas import CourseCreate, CourseOut, MaterialOut
from app.services.document_service import SUPPORTED_EXTENSIONS, safe_filename, validate_upload_bytes
from app.services.ingestion_service import ingest_material

router = APIRouter(prefix="/courses", tags=["courses"])

@router.get("", response_model=list[CourseOut])
def list_courses(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.scalars(select(Course).where(Course.owner_id == user.id).order_by(Course.id)).all()

@router.post("", response_model=CourseOut, status_code=201)
def create_course(payload: CourseCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    course = Course(title=payload.title, description=payload.description, owner_id=user.id)
    db.add(course); db.commit(); db.refresh(course)
    return course

@router.get("/{course_id}", response_model=CourseOut)
def get_course(course_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return owned_course(course_id, user, db)

@router.get("/{course_id}/materials", response_model=list[MaterialOut])
def list_materials(course_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    owned_course(course_id, user, db)
    return db.scalars(select(Material).where(Material.course_id == course_id).order_by(Material.id.desc())).all()

@router.post("/{course_id}/materials", response_model=MaterialOut, status_code=201)
def upload_material(
    course_id: int,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    owned_course(course_id, user, db)
    original = file.filename or "upload"
    ext = Path(original).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=415, detail="Only PDF and DOCX files are supported")
    data = file.file.read()
    if len(data) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large")
    try:
        validate_upload_bytes(original, data)
    except ValueError as exc:
        raise HTTPException(status_code=415, detail=str(exc))
    stored = settings.upload_path / f"{uuid4().hex}_{safe_filename(original)}"
    stored.write_bytes(data)
    material = Material(
        course_id=course_id,
        title=Path(original).stem,
        original_filename=original,
        stored_path=str(stored),
        mime_type=file.content_type or "application/octet-stream",
    )
    db.add(material); db.commit(); db.refresh(material)
    try:
        ingest_material(db, material)
    except Exception:
        pass
    db.refresh(material)
    return material
