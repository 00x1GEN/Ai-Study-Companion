from pathlib import Path
from io import BytesIO
from zipfile import ZipFile, BadZipFile
from pypdf import PdfReader
from docx import Document
from app.core.config import settings

SUPPORTED_EXTENSIONS = {".pdf", ".docx"}

def safe_filename(name: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in name)
    return cleaned[:180] or "upload"

def extract_text(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    if ext == ".docx":
        doc = Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError("Unsupported file type")

def chunks(text: str) -> list[str]:
    text = " ".join(text.split())
    if not text:
        return []
    size = settings.rag_chunk_size
    overlap = settings.rag_chunk_overlap
    result, start = [], 0
    while start < len(text):
        end = min(len(text), start + size)
        chunk = text[start:end].strip()
        if chunk:
            result.append(chunk)
        if end == len(text):
            break
        start = max(start + 1, end - overlap)
    return result


def validate_upload_bytes(filename: str, data: bytes) -> None:
    ext = Path(filename).suffix.lower()
    if ext == ".pdf":
        if not data.startswith(b"%PDF"):
            raise ValueError("File content is not a valid PDF signature")
        return
    if ext == ".docx":
        try:
            with ZipFile(BytesIO(data)) as archive:
                names = set(archive.namelist())
                if "word/document.xml" not in names:
                    raise ValueError("DOCX archive is missing word/document.xml")
        except BadZipFile as exc:
            raise ValueError("File content is not a valid DOCX archive") from exc
        return
    raise ValueError("Unsupported file type")
