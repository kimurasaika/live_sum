# prime-directive

Hard constraints for this project. Non-negotiable.

- Fully offline at runtime. No cloud ASR APIs, no telemetry, anywhere in the runtime path.
- Audio never leaves local disk. No cloud storage, no third-party upload of audio.
- ASR runs on CPU, must support Thai, prioritizes accuracy and speed.
- Live path: browser mic → WebSocket → backend ASR. No client-side ASR.
- Backend: Python + FastAPI. Do not introduce a second backend framework.

One-time network exceptions (setup only, never at runtime): model downloads (HF hub), `yt-dlp`/`gtts` for fetching test/sample audio.

**⚠ EXCEPTION — user-confirmed, summarization only**: summarization may call a cloud LLM
(OpenRouter) instead of the local mT5 pipeline, controlled by `SUMMARIZER_BACKEND` env var
(`local` default, `openrouter` opt-in). This means the derived text transcript — not audio —
can leave the machine when this backend is explicitly enabled. ASR/audio path is unaffected and
stays local always. See `PROGRESS.md` Completed Tasks for the confirmation record and
`skills/cipher-sanctum.md` for the security note. Do not silently assume "fully offline" holds
for summarization without checking `SUMMARIZER_BACKEND` first.
