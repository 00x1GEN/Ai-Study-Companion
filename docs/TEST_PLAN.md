# Test Plan

## Authentication
- valid login
- invalid password
- duplicate registration
- refresh rotation
- reuse of revoked refresh token
- expired refresh token
- protected endpoint without token

## Files
- PDF upload
- DOCX upload
- unsupported extension
- oversized file
- empty/extraction failure
- course ownership isolation

## RAG
- relevant source retrieval
- no matching source
- cross-course isolation
- prompt injection inside source material
- provider timeout/error
- invalid provider output
- citation/source traceability

## Learning
- flashcard known/unknown review
- Leitner box progression
- quiz partial/perfect score
- XP calculation
- level boundary
- streak same-day
- streak next-day
- streak reset
- badge award idempotency

## Infrastructure
- clean docker compose startup
- restart persistence
- backup and restore
- health/readiness checks
- CI lint/test/build gates
- rollback from failed release
