# AI Study Companion — RC1 Release Notes

Status: **RC1-CONDITIONAL**

Major RC1 corrections:

- Added real Alembic initial migration and pgvector/HNSW schema.
- Added container entrypoint: migrate → idempotent seed → API start.
- Corrected pgvector clean-database initialization path.
- Corrected gamification transaction boundary.
- Corrected mock AI structured generation for offline verification.
- Added mobile registration.
- Replaced hardcoded AI Chat course ID with course selector.
- Defaulted AI Chat to mock provider for key-free development.
- Removed unused mobile imports.
- Added host-side RC1 smoke script.

Open release gates: Docker/PostgreSQL runtime and Flutter SDK checks must pass on the release host.
