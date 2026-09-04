# Security Baseline

- Passwords are bcrypt-hashed.
- Access tokens are short-lived JWTs.
- Refresh tokens are random opaque secrets stored server-side only as SHA-256 hashes.
- Refresh tokens rotate on use and can be revoked.
- Uploaded files are renamed and limited to PDF/DOCX.
- Maximum file size is configurable.
- Course ownership is enforced before retrieval and learning operations.
- RAG retrieval is filtered by course before vector similarity ranking.
- AI system prompt explicitly ignores instructions found in untrusted source documents.
- API secrets are provided only through environment variables.
- No provider API key belongs in Flutter/mobile source code.
- Production deployments should terminate TLS at a trusted ingress/reverse proxy and use managed secrets.
