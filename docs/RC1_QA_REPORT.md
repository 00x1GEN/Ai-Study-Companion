# AI Study Companion — RC1.1 Reverification QA Report

## Release status

**RC1.1 status: CONDITIONAL PASS**

The source package has been re-audited and corrected. All checks executable in this environment pass. Docker/PostgreSQL runtime, Flutter analyzer/test, and live provider calls remain external release gates because Docker, Flutter SDK, provider keys and provider network access are unavailable in this environment.

## Checks executed

- Python application/test/Alembic syntax compilation: PASS
- Docker Compose and GitHub Actions YAML parsing: PASS
- Shell syntax for entrypoint, smoke, backup and restore scripts: PASS
- Dependency-light executable tests: **10 PASSED**
- Static Python unused-import scan: PASS
- Static ORM ↔ Alembic table/column consistency review: PASS
- Official API contract review: OpenAI Responses/Embeddings, Anthropic Messages, Gemini generation/embeddings, pgvector SQLAlchemy/Psycopg patterns reviewed against current primary documentation

## Findings and disposition

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| RC1-001 | Blocker | Initial Alembic migration missing | Fixed in RC1 |
| RC1-002 | Blocker | Container startup did not migrate/seed | Fixed in RC1 |
| RC1-003 | High | pgvector initialization order unsafe on clean DB | Fixed; migration owns extension creation and pooled connections only register adapter |
| RC1-004 | High | Mock AI generation did not return JSON | Fixed in RC1 |
| RC1-005 | High | Gamification helper committed partial operations | Fixed in RC1 |
| RC1-006 | Medium | AI Chat used hardcoded course ID | Fixed in RC1 |
| RC1-007 | Medium | Mobile default provider required an API key | Fixed in RC1 |
| RC1-008 | Medium | Registration UI missing | Fixed in RC1 |
| RC1.1-013 | High | New registered user could not create a first course | Fixed: Create Course UI added |
| RC1.1-014 | High | Mobile logout cleared local tokens without revoking server refresh token | Fixed: backend logout is called before local clear |
| RC1.1-015 | High | Refresh token rotation had a concurrent double-use race | Fixed: database row lock added |
| RC1.1-016 | High | Stored embeddings did not record provider/model/dimensions | Fixed: metadata columns + compatibility filter + migration 0002 |
| RC1.1-017 | High | AI JSON generation could fail on fenced JSON and accept empty/invalid quizzes | Fixed: robust parser and strict validation |
| RC1.1-018 | High | Repeated quiz submissions could repeatedly award XP | Fixed: repeat attempts award 0 XP |
| RC1.1-019 | High | Flashcards could be repeatedly rated before due date to farm XP | Fixed: due-date filtering and early return |
| RC1.1-020 | High | CI ran pytest without database migrations | Fixed: Alembic + seed added before tests |
| RC1.1-021 | High | Docker ENTRYPOINT ignored make test/migrate/seed commands | Fixed: explicit command passthrough |
| RC1.1-022 | Medium | Backup/restore ignored custom Compose database env values | Fixed: commands use DB container environment |
| RC1.1-023 | Medium | Upload accepted extension without validating basic PDF/DOCX structure | Fixed: signature/OpenXML structure validation |
| RC1.1-024 | Medium | AI generation could run without source material | Fixed: 409 precondition for empty course context |
| RC1.1-025 | Modernization | Authentication used older passlib/python-jose pattern | Updated to pwdlib Argon2 + PyJWT following current FastAPI guidance |
| RC1.1-026 | Quality | Generation defaults used older/high-cost model choices | Updated defaults to gpt-5.6-terra and claude-sonnet-5; Gemini remains gemini-2.5-flash |

## New full integration gate prepared

`backend/tests/test_api_integration.py` now exercises register → refresh rotation → course creation → DOCX upload/ingestion → pgvector-backed RAG → flashcard generation/review → quiz generation/submission → gamification/progress → logout/revocation.

GitHub Actions now applies Alembic migrations and seed data before running the complete test suite.

## Mandatory host gate

```bash
cp .env.example .env
./scripts/rc1_host_smoke.sh
```

Run this on a workstation with Docker installed. Install Flutter as well if mobile `flutter analyze` and `flutter test` are to be executed in the same gate.

## Known limitations that are not release-code defects

- Document ingestion is synchronous; large files or slow external embedding APIs can increase request time.
- Scanned/image-only PDFs require OCR, which is not part of RC1.1.
- Antivirus/malware scanning for uploads is not included.
- API rate limiting and production secret-management infrastructure are deployment responsibilities, not implemented application features.
- Changing embedding provider/model/dimensions requires re-ingesting existing materials.
- Live OpenAI/Claude/Gemini quality, account permissions, quotas, pricing and latency must be validated with the actual institutional API accounts.

## Release recommendation

Do not label this package FINAL/PRODUCTION until the host smoke script passes Docker/PostgreSQL/pgvector and Flutter gates. For student verification work it is suitable as **RC1.1-CONDITIONAL** and intentionally contains explicit testable responsibilities.