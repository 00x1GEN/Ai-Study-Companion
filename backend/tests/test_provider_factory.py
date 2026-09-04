from app.ai.providers import generation_provider, MockGenerationProvider

def test_mock_provider_factory():
    p = generation_provider("mock")
    assert isinstance(p, MockGenerationProvider)
