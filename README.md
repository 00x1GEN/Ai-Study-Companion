# AI Study Companion — Production-Oriented Full Software Package

Mentor-prepared reference implementation for the Aspira professional practice project.

## Included

- Flutter mobile client
- FastAPI REST API
- PostgreSQL + pgvector
- PDF/DOCX ingestion
- RAG with real OpenAI / Anthropic Claude / Google Gemini generation providers
- OpenAI / Gemini embeddings
- JWT access + rotating refresh tokens
- Flashcards, quizzes, XP, levels, badges, achievements and streaks
- Docker Compose deployment
- Nginx reverse proxy
- GitHub Actions CI/CD
- Unit/integration/API tests
- Seed/demo data
- Provider fallback for development without paid AI keys

## Quick start

1. Copy environment file:

```bash
cp .env.example .env
```

2. Start infrastructure and API:

```bash
docker compose up --build
```

3. Open API docs:

- http://localhost:8000/docs

4. Run Flutter app separately:

```bash
cd mobile
flutter pub get
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000/api/v1
```

Android emulator uses `10.0.2.2` to reach the host machine.

## Demo account

- `student@aspira.test`
- `password123`

## AI configuration

Set `AI_PROVIDER` to:

- `openai`
- `anthropic`
- `gemini`
- `mock`

Set `EMBEDDING_PROVIDER` to:

- `openai`
- `gemini`
- `mock`

Anthropic is used as a generation provider. Embeddings are supplied separately by OpenAI, Gemini or the deterministic mock embedding provider.

## Important academic rule

This repository is a mentor baseline/reference solution. Students must not claim the supplied baseline source code as their own work. Their contribution should be evidenced through verification, testing, defect analysis, approved fixes, integration, data preparation, documentation and release-readiness work.

## Validation before student distribution

Run the complete host gate on a workstation with Docker and Flutter installed:

```bash
cp .env.example .env
./scripts/rc1_host_smoke.sh
```

The script validates Compose, starts a clean PostgreSQL/pgvector stack, applies Alembic migrations, loads seed data, runs backend integration tests, verifies API smoke endpoints and runs Flutter analyze/test when Flutter is installed.

If you change `EMBEDDING_PROVIDER`, `OPENAI_EMBEDDING_MODEL`, `GEMINI_EMBEDDING_MODEL`, or `EMBEDDING_DIMENSIONS` after materials have already been ingested, re-ingest those materials so document and query vectors remain in the same embedding space.
