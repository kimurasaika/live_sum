# prime-directive

Hard constraints for this project. Non-negotiable.

- Fully offline at runtime. No cloud ASR/LLM APIs, no telemetry, anywhere in the runtime path.
- Audio and transcripts never leave local disk. No cloud storage, no third-party upload.
- ASR runs on CPU, must support Thai, prioritizes accuracy and speed.
- Summarization runs on a local transformers pipeline — no server dependency (no Ollama).
- Live path: browser mic → WebSocket → backend ASR. No client-side ASR.
- Backend: Python + FastAPI. Do not introduce a second backend framework.

One-time network exceptions (setup only, never at runtime): model downloads (HF hub), `yt-dlp`/`gtts` for fetching test/sample audio.
