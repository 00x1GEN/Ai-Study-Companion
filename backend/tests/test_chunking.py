from app.services.document_service import chunks

def test_chunking_short_text():
    assert chunks("hello world") == ["hello world"]

def test_chunking_empty_text():
    assert chunks("   ") == []

def test_chunking_long_text_has_multiple_chunks():
    result = chunks("abc " * 1000)
    assert len(result) > 1
    assert all(result)
