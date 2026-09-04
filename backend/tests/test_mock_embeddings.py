from app.ai.providers import MockEmbeddingProvider
from app.core.config import settings

def test_mock_embedding_dimensions_and_determinism():
    p = MockEmbeddingProvider()
    a = p.embed(["stack queue"])[0]
    b = p.embed(["stack queue"])[0]
    assert len(a) == settings.embedding_dimensions
    assert a == b
