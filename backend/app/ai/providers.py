from abc import ABC, abstractmethod
import math
import hashlib
from app.core.config import settings

class GenerationProvider(ABC):
    name: str

    @abstractmethod
    def generate(self, system: str, user: str) -> str:
        raise NotImplementedError

class EmbeddingProvider(ABC):
    name: str
    model_name: str

    @abstractmethod
    def embed(self, texts: list[str], *, task: str = "document") -> list[list[float]]:
        raise NotImplementedError

class MockGenerationProvider(GenerationProvider):
    name = "mock"
    def generate(self, system: str, user: str) -> str:
        if '"question":"...", "answer":"..."' in user:
            return '[{"question":"What is a stack?","answer":"A LIFO data structure."},{"question":"What is a queue?","answer":"A FIFO data structure."},{"question":"What does RAG add before generation?","answer":"Relevant retrieved source context."},{"question":"Why use embeddings?","answer":"To represent semantic meaning as vectors."},{"question":"What should grounded AI do when context is insufficient?","answer":"State that the available context is insufficient."}]'
        if '"correct_index"' in user:
            return '[{"question":"Which structure uses FIFO?","options":["Stack","Queue","Tree","Graph"],"correct_index":1,"explanation":"A queue follows FIFO ordering."},{"question":"What does RAG retrieve?","options":["Source context","Passwords","UI themes","Docker images"],"correct_index":0,"explanation":"RAG retrieves relevant source context before generation."}]'
        return "MOCK AI RESPONSE\n\n" + user[-1200:]

class MockEmbeddingProvider(EmbeddingProvider):
    name = "mock"
    model_name = "mock-hash"
    def embed(self, texts: list[str], *, task: str = "document") -> list[list[float]]:
        dim = settings.embedding_dimensions
        out = []
        for text in texts:
            vec = [0.0] * dim
            words = text.lower().split()
            for word in words:
                digest = hashlib.sha256(word.encode()).digest()
                idx = int.from_bytes(digest[:4], "big") % dim
                sign = 1.0 if digest[4] % 2 == 0 else -1.0
                vec[idx] += sign
            norm = math.sqrt(sum(x*x for x in vec)) or 1.0
            out.append([x / norm for x in vec])
        return out

class OpenAIGenerationProvider(GenerationProvider):
    name = "openai"
    def __init__(self):
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured")
        from openai import OpenAI
        self.client = OpenAI(api_key=settings.openai_api_key)
    def generate(self, system: str, user: str) -> str:
        response = self.client.responses.create(
            model=settings.openai_model,
            instructions=system,
            input=user,
        )
        return response.output_text

class OpenAIEmbeddingProvider(EmbeddingProvider):
    name = "openai"
    def __init__(self):
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured")
        from openai import OpenAI
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model_name = settings.openai_embedding_model
    def embed(self, texts: list[str], *, task: str = "document") -> list[list[float]]:
        response = self.client.embeddings.create(
            model=settings.openai_embedding_model,
            input=texts,
            dimensions=settings.embedding_dimensions,
        )
        return [row.embedding for row in response.data]

class AnthropicGenerationProvider(GenerationProvider):
    name = "anthropic"
    def __init__(self):
        if not settings.anthropic_api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not configured")
        import anthropic
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    def generate(self, system: str, user: str) -> str:
        message = self.client.messages.create(
            model=settings.anthropic_model,
            max_tokens=4096,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return "".join(block.text for block in message.content if getattr(block, "type", "") == "text")

class GeminiGenerationProvider(GenerationProvider):
    name = "gemini"
    def __init__(self):
        if not settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")
        from google import genai
        self.client = genai.Client(api_key=settings.gemini_api_key)
    def generate(self, system: str, user: str) -> str:
        from google.genai import types
        response = self.client.models.generate_content(
            model=settings.gemini_model,
            contents=user,
            config=types.GenerateContentConfig(system_instruction=system),
        )
        return response.text or ""

class GeminiEmbeddingProvider(EmbeddingProvider):
    name = "gemini"
    def __init__(self):
        if not settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")
        from google import genai
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model_name = settings.gemini_embedding_model
    def embed(self, texts: list[str], *, task: str = "document") -> list[list[float]]:
        from google.genai import types
        task_type = "RETRIEVAL_QUERY" if task == "query" else "RETRIEVAL_DOCUMENT"
        response = self.client.models.embed_content(
            model=settings.gemini_embedding_model,
            contents=texts,
            config=types.EmbedContentConfig(
                task_type=task_type,
                output_dimensionality=settings.embedding_dimensions,
            ),
        )
        return [list(item.values) for item in response.embeddings]

def generation_provider(name: str | None = None) -> GenerationProvider:
    selected = (name or settings.ai_provider).lower()
    if selected == "openai":
        return OpenAIGenerationProvider()
    if selected == "anthropic":
        return AnthropicGenerationProvider()
    if selected == "gemini":
        return GeminiGenerationProvider()
    return MockGenerationProvider()

def embedding_provider() -> EmbeddingProvider:
    selected = settings.embedding_provider.lower()
    if selected == "openai":
        return OpenAIEmbeddingProvider()
    if selected == "gemini":
        return GeminiEmbeddingProvider()
    return MockEmbeddingProvider()
