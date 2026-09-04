from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    app_name: str = "AI Study Companion"
    api_v1_prefix: str = "/api/v1"
    secret_key: str = "replace-me"
    access_token_minutes: int = 20
    refresh_token_days: int = 14

    database_url: str = "postgresql+psycopg://ai_study:change-me@localhost:5432/ai_study"
    upload_dir: str = "/data/uploads"
    max_upload_mb: int = 25
    cors_origins: str = "http://localhost:3000,http://localhost:8080"

    ai_provider: str = "mock"
    embedding_provider: str = "mock"

    openai_api_key: str = ""
    openai_model: str = "gpt-5.6-terra"
    openai_embedding_model: str = "text-embedding-3-small"

    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-5"

    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.6-flash"
    gemini_embedding_model: str = "gemini-embedding-001"

    embedding_dimensions: int = 1536
    rag_top_k: int = 6
    rag_chunk_size: int = 1000
    rag_chunk_overlap: int = 150
    log_level: str = "INFO"

    @property
    def cors_origin_list(self) -> list[str]:
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]

    @property
    def upload_path(self) -> Path:
        p = Path(self.upload_dir)
        p.mkdir(parents=True, exist_ok=True)
        return p

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
