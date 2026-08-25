# TASK.md — Current Task

## Task Name
Add optional cloud LLM summarization backend (OpenRouter) — explicit deviation from offline-only

## What This Task Requires
**DEVIATION FROM AGENTS.md HARD CONSTRAINT, USER-CONFIRMED**: AGENTS.md's "Fully offline"
constraint is relaxed for summarization only, per explicit user decision (asked directly:
"ยกเว้นเฉพาะ summarize ใช้ OpenRouter API ได้"). ASR stays 100% local — audio never leaves the
machine. Only the derived text transcript may be sent to OpenRouter when this backend is
explicitly enabled. AGENTS.md itself is not edited (protocol: only the human changes it) — this
deviation is logged in PROGRESS.md and in `skills/prime-directive.md` instead.

1. `backend/summarize.py`: add an OpenRouter-backed summarizer function alongside the existing
   local mT5 one. Config via env vars: `OPENROUTER_API_KEY`, `OPENROUTER_MODEL`,
   `SUMMARIZER_BACKEND` (`local` | `openrouter`, default `local` — cloud is opt-in, never the
   silent default).
2. `.env.example`: template with the three vars above, no real key.
3. `.gitignore`: add `.env` (real file with the user's key must never be committed).
4. `requirements.txt`: add `python-dotenv` (load `.env`) and `openai` (OpenRouter is
   OpenAI-API-compatible, reuse that SDK rather than hand-roll HTTP).
5. `backend/main.py`: no change to call sites — `summarize_text()` stays the single entry
   point, it internally dispatches to local or OpenRouter based on `SUMMARIZER_BACKEND`.

## Files In Scope
- backend/summarize.py
- .env.example
- .gitignore
- requirements.txt

## Files Out Of Scope
- backend/main.py, backend/asr.py — no changes; ASR stays local-only, unaffected
- AGENTS.md — never edited by the agent, per protocol

## Acceptance Criteria
1. With `SUMMARIZER_BACKEND` unset or `local`: behavior identical to before (mT5, no network
   call) — `python test_asr.py`-style smoke check unaffected.
2. With `SUMMARIZER_BACKEND=openrouter` and a real `OPENROUTER_API_KEY` set (user provides
   their own key, not committed): `summarize_text()` returns a real OpenRouter completion,
   verified with an actual API call once the user has added their key.
3. `.env` is gitignored; `.env.example` has no real secret and is committed.

## Approach
1. `.env.example` + `.gitignore` update first (cheap, no code risk).
2. `summarize.py`: keep `get_summarizer()`/local path as-is; add
   `_summarize_openrouter(text)` using the `openai` SDK pointed at
   `base_url="https://openrouter.ai/api/v1"`. `summarize_text()` branches on
   `os.getenv("SUMMARIZER_BACKEND", "local")`.
3. Load `.env` via `python-dotenv` at process start (`load_dotenv()` in `summarize.py` or
   `main.py` — pick one place, avoid double-loading).
4. Verify local path still works unchanged (default). Verify OpenRouter path once user has
   supplied a real key — cannot self-verify without one.

## Known Risks
- Model id for the "free" OpenRouter model the user mentioned was garbled in chat ("oxalpha")
  — not guessing a specific model slug. `OPENROUTER_MODEL` is a required env var the user must
  set themselves to the exact free model slug from their OpenRouter account.
- This is a real, permanent architecture exception, not a toggle to forget about — flagged
  loudly in PROGRESS.md and `skills/prime-directive.md`/`skills/cipher-sanctum.md` so it isn't
  silently re-assumed "offline" in a future session.
- Never log or print the API key. Never commit `.env`.
