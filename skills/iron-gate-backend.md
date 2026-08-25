# iron-gate-backend

FastAPI backend guide. Files: `backend/main.py`, `backend/asr.py`, `backend/summarize.py`.

- `GET /` serves `frontend/index.html`; `/static` mounts `frontend/`.
- `WS /ws/asr` — live mic path. Receives raw audio bytes per chunk, returns transcript text.
  - **Known bug (unfixed):** `asr_socket` calls `transcribe_chunk()` synchronously inside the
    async handler. CPU-bound work blocks the event loop, so WebSocket keepalive pings can't be
    answered during transcription — connection dies with `keepalive ping timeout` before any
    reply is sent. Fix: wrap the call in `loop.run_in_executor(...)`.
  - **Missing entirely:** live summarization. `summarize_text()` is never called from this path —
    only from the offline batch script. There is no accumulate-and-summarize loop on the live
    transcript stream.
- `backend/asr.py`: `faster-whisper`, `WhisperModel("small", device="cpu", compute_type="int8")`
  hardcoded. Model choice is a known open tradeoff — see `chronicle-of-changes.md`.
- `backend/summarize.py`: `csebuetnlp/mT5_multilingual_XLSum` via `transformers.pipeline`,
  chunks input text at 2000 chars, joins per-chunk summaries with blank lines.
