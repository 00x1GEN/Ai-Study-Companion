import pytest
from app.ai.providers import OpenAIGenerationProvider, AnthropicGenerationProvider, GeminiGenerationProvider
from app.core.config import settings


def test_unconfigured_real_generation_providers_fail_fast(monkeypatch):
    monkeypatch.setattr(settings, 'openai_api_key', '')
    monkeypatch.setattr(settings, 'anthropic_api_key', '')
    monkeypatch.setattr(settings, 'gemini_api_key', '')
    with pytest.raises(RuntimeError): OpenAIGenerationProvider()
    with pytest.raises(RuntimeError): AnthropicGenerationProvider()
    with pytest.raises(RuntimeError): GeminiGenerationProvider()
