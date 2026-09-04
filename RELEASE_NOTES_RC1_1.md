# AI Study Companion RC1.1 — Reverification Fixes

Additional QA after RC1 found and fixed:

- server-side refresh-token rotation now locks the token row to prevent concurrent double rotation;
- mobile logout now revokes the server refresh token before clearing secure storage;
- registered users can create their first course from the mobile app;
- AI JSON parsing tolerates fenced JSON and rejects invalid/empty generated quizzes;
- quiz repeat attempts no longer award repeat XP;
- PDF/DOCX uploads validate basic file signatures/content structure;
- stored materials record embedding provider/model/dimensions and RAG retrieval rejects incompatible vector spaces;
- Gemini embeddings use retrieval document/query task types;
- configured real AI providers fail with clear missing-key errors;
- default OpenAI/Anthropic models updated to current cost-balanced models.
