from io import BytesIO
from zipfile import ZipFile
import pytest
from app.services.document_service import validate_upload_bytes

def test_pdf_signature():
    validate_upload_bytes("a.pdf", b"%PDF-1.7 test")
    with pytest.raises(ValueError): validate_upload_bytes("a.pdf", b"not pdf")

def test_docx_signature():
    bio=BytesIO()
    with ZipFile(bio,"w") as z: z.writestr("word/document.xml","<w:document/>")
    validate_upload_bytes("a.docx", bio.getvalue())
    with pytest.raises(ValueError): validate_upload_bytes("a.docx", b"PKbad")
