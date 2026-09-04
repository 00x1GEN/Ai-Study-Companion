from typing import Literal
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    course_id: int
    message: str = Field(min_length=2, max_length=6000)
    provider: Literal["openai", "anthropic", "gemini", "mock"] | None = None

class SourceOut(BaseModel):
    material_id: int
    chunk_id: int
    title: str
    excerpt: str
    distance: float

class ChatResponse(BaseModel):
    answer: str
    provider: str
    sources: list[SourceOut]

class GenerateRequest(BaseModel):
    course_id: int
    count: int = Field(default=5, ge=1, le=20)

class GeneratedCount(BaseModel):
    created: int
