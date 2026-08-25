# TASK.md — Current Task

## Task Name
Fix live WebSocket blocking bug + swap backend/asr.py engine to Typhoon NeMo ASR

## What This Task Requires
1. `backend/asr.py`: replace `faster-whisper`/`WhisperModel` with NeMo
   `typhoon-ai/typhoon-asr-streaming-115m` via `ASRModel.from_pretrained()` — the model
   verified fastest+most-accurate on real audio in the prior spike (see PROGRESS.md).
   `transcribe_chunk(audio_bytes) -> str` keeps the same signature so callers don't change.
2. `backend/main.py`: fix the confirmed event-loop-blocking bug — wrap the synchronous
   `transcribe_chunk()` call in `loop.run_in_executor(None, ...)` inside `asr_socket` so
   WebSocket keepalive pings aren't starved during transcription.
3. `requirements.txt`: add `nemo_toolkit[asr]` (already installed locally this session).

## Files In Scope
- backend/asr.py
- backend/main.py
- requirements.txt

## Files Out Of Scope
- frontend/* — no UI changes this task
- backend/summarize.py — live summarization wiring is a separate, later task (explicitly
  deferred, not part of this one)

## Acceptance Criteria
1. `python test_asr.py` exits 0, transcript matches >=3/4 expected words (now via the new
   NeMo-based `transcribe_chunk`).
2. Live WebSocket check: start `uvicorn backend.main:app`, connect via a WS client, send a
   real audio chunk, receive a transcript reply within a reasonable time (no ping-timeout
   disconnect, no silent hang) — proves the blocking fix actually works, not just that the
   code compiles.

## Approach
1. Rewrite `get_model()`/`transcribe_chunk()` in `backend/asr.py`: pydub preprocess to
   16kHz mono (unchanged), write to a temp wav file (NeMo's `ASRModel.transcribe()` takes
   file paths, not in-memory buffers — confirmed in `scripts/bench_typhoon_nemo.py`), call
   `model.transcribe([tmp_path])`, clean up temp file.
2. In `backend/main.py`, get the running loop and dispatch `transcribe_chunk` via
   `run_in_executor` instead of calling it directly.
3. Re-run `test_asr.py` to verify accuracy holds with the new engine.
4. Re-run the live WS test script (`scripts/test_live_ws.py`) against a freshly started
   server to confirm the blocking fix.

## Known Risks
- NeMo model load time (~16-30s cold start, per prior bench) still happens on first
  WebSocket message even with the executor fix — first chunk will be slow, just no longer
  blocking (loop stays responsive to pings while it loads in the thread pool).
- `run_in_executor(None, ...)` uses the default `ThreadPoolExecutor` — fine for one user;
  if concurrent connections both trigger cold model loads, they'll race on `_model is None`
  (not thread-safe) — acceptable for this project's single-user local scope, flagging it,
  not fixing it (out of scope creep).
- Temp file per chunk on Windows — must close the file handle before `pydub` export writes
  to it, and before NeMo reads it, or it'll hit a file-lock error (Windows-specific, unlike
  Linux/Mac).
