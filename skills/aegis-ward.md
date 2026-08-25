# aegis-ward

Security / offline-safety guide.

- Threat model is narrow but strict: this handles potentially sensitive meeting audio, so the
  one rule that matters most is **audio never leaves the machine**. No outbound calls carrying
  audio, anywhere in the runtime path.
- **Exception, user-confirmed**: summarization *text* (the derived transcript, not audio) may
  be sent to OpenRouter when `SUMMARIZER_BACKEND=openrouter` is explicitly set — see
  `prime-directive.md`. Default stays `local` (no network). Anyone auditing this project should
  check that env var before assuming transcripts stay on-disk.
- WebSocket endpoint (`/ws/asr`) has no auth, no origin check — fine for localhost-only use as
  currently scoped. If this is ever exposed beyond `127.0.0.1`, that gap needs closing first.
- One-time setup network calls (model downloads, `yt-dlp`) are an accepted exception for
  setup — never let them slide into the runtime path.
- Secrets: `OPENROUTER_API_KEY` lives in `.env` only (gitignored). `.env.example` documents the
  shape with no real value. Never log or print the key. Before any commit, check
  `git status`/diff doesn't include `.env` — `.gitignore` covers it but double-check anyway
  since a leaked API key is a real, hard-to-undo exposure.
