# aegis-ward

Security / offline-safety guide.

- Threat model is narrow but strict: this handles potentially sensitive meeting audio, so the
  one rule that matters most is **nothing leaves the machine**. No outbound calls in the runtime
  path — verify any new dependency doesn't phone home before adding it.
- WebSocket endpoint (`/ws/asr`) has no auth, no origin check — fine for localhost-only use as
  currently scoped. If this is ever exposed beyond `127.0.0.1`, that gap needs closing first.
- One-time setup network calls (model downloads, `yt-dlp`) are the only accepted exception —
  never let them slide into the runtime path.
- No secrets/API keys anywhere in this project (by design — everything runs local models).
  If any get added later (e.g. for a hosted model), they must never be committed — check
  `.gitignore` covers them.
