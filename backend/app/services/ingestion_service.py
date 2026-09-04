from pathlib import Path
from sqlalchemy.orm import Session
from app.models import Material, DocumentChunk
from app.services.document_service import extract_text, chunks
from app.ai.providers import embedding_provider
from app.core.config import settings

def ingest_material(db: Session, material: Material):
    try:
        text = extract_text(Path(material.stored_path))
        parts = chunks(text)
        if not parts:
            raise ValueError("No extractable text found")
        provider = embedding_provider()
        vectors = provider.embed(parts, task="document")
        if len(vectors) != len(parts):
            raise ValueError("Embedding provider returned an unexpected vector count")
        for vector in vectors:
            if len(vector) != settings.embedding_dimensions:
                raise ValueError("Embedding provider returned an unexpected vector dimension")
        for i, (content, vector) in enumerate(zip(parts, vectors)):
            db.add(DocumentChunk(
                material_id=material.id,
                course_id=material.course_id,
                chunk_index=i,
                content=content,
                embedding=vector,
            ))
        material.chunk_count = len(parts)
        material.embedding_provider = provider.name
        material.embedding_model = provider.model_name
        material.embedding_dimensions = settings.embedding_dimensions
        material.status = "ready"
        material.error_message = None
        db.commit()
    except Exception as exc:
        db.rollback()
        material = db.get(Material, material.id)
        material.status = "failed"
        material.error_message = str(exc)[:1000]
        db.commit()
        raise
