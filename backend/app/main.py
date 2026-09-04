from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import ensure_extensions
from app.core.logging import configure_logging
from app.api.router import router
from app.services.gamification_service import seed_badges
from app.core.database import SessionLocal

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    ensure_extensions()
    with SessionLocal() as db:
        seed_badges(db)
    yield

app = FastAPI(title=settings.app_name, version="2.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router, prefix=settings.api_v1_prefix)

@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.app_env}

@app.get("/ready")
def ready():
    return {"status": "ready"}
