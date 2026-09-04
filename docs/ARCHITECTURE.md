# Architecture

Mobile Flutter client
→ HTTPS REST API / FastAPI
→ authentication and domain services
→ PostgreSQL + pgvector
→ document ingestion
→ embedding provider
→ vector retrieval
→ RAG generation provider

Generation provider is independently configurable:
OpenAI / Anthropic Claude / Gemini / Mock.

Embedding provider is independently configurable:
OpenAI / Gemini / deterministic Mock.

This separation allows Claude to generate answers while OpenAI or Gemini supplies embeddings.

## Embedding dimensionality

RC1 fixes the database vector column at 1536 dimensions. If a different embedding dimension is selected later, a new Alembic migration must alter/rebuild the vector column and HNSW index before switching providers. Do not change `EMBEDDING_DIMENSIONS` in an existing database without a schema migration.

## Gemini embedding model decision

`gemini-embedding-001` is intentionally retained for the current text-chunk ingestion path. The newer `gemini-embedding-2` is the latest Gemini embedding model, but when multiple inputs are supplied it produces an aggregated embedding rather than one independent embedding per input. This application ingests batches of text chunks and requires one vector per chunk. Migrating to `gemini-embedding-2` therefore requires either one request per chunk or a dedicated batch workflow and should be treated as a separate architecture change.
