# CONTEXT.md — Architecture Reference

## Project Overview
Offline meeting-summarizer web app. Browser captures microphone audio and
streams it over WebSocket to a FastAPI backend. Backend runs real-time
Thai-language ASR on CPU to produce a live transcript. After the meeting,
the accumulated transcript is fed to a local transformers summarization
pipeline to produce a meeting summary. Nothing leaves local disk.

## Tech Stack
Runtime:          Python (FastAPI backend, ASGI via uvicorn)
Framework:        FastAPI + WebSocket, static HTML/JS frontend for mic capture
ASR:              faster-whisper (CTranslate2), Thai language, CPU int8 quantized — [TO BE VERIFIED: model size vs. latency/accuracy tradeoff]
Summarization:    HuggingFace transformers pipeline, multilingual/Thai-capable — [TO BE DEFINED: exact model, candidate csebuetnlp/mT5_multilingual_XLSum]
Database:         None planned yet
External Services:None (offline-only constraint)
Deployment:       Local machine only (no deployment target defined)

## Core Modules
- `backend/asr.py` — Typhoon NeMo (`typhoon-ai/typhoon-asr-streaming-115m`) ASR wrapper.
  `transcribe_chunk()` auto-chunks input over `CHUNK_MS` (20s) before calling NeMo `transcribe()`
  to avoid O(n^2) Conformer self-attention memory blowup on long audio.
- `backend/summarize.py` — summarization wrapper, `local` (mT5) or `openrouter` (cloud LLM)
  backend selected via `SUMMARIZER_BACKEND` env var.
- `backend/main.py` — FastAPI app. Routes: `/` (landing), `/asr` (realtime page), `/upload`
  (file-upload page), `POST /api/upload` (batch ASR + summarize), `WS /ws/asr` (live mic
  streaming). `warm_up_models()` runs on startup, main thread, to avoid a Windows numba JIT
  deadlock if the first NeMo transcribe happened lazily in a worker thread.
- `frontend/index.html` — landing page linking to both modes.
- `frontend/asr.html` + `frontend/app.js` — realtime mode: mic capture → WebSocket → live
  transcript + rolling-window summary.
- `frontend/upload.html` + `frontend/upload.js` — file-upload mode: pick file → POST
  `/api/upload` → full transcript + one summary.
- `frontend/style.css` — shared MUJI-style theme (off-white/beige, minimal borders, no shadows).
- `Dockerfile` — `python:3.11-slim` + `ffmpeg` (pydub dependency), serves on `:8080`. Models
  download on first container start, not baked into the image.

## Off-Limits Zones
No explicit off-limits zones beyond offline-only constraint. Defer to
AGENTS.md Hard Constraints. Note: the OpenRouter summarize backend is a user-confirmed,
scoped exception to the offline constraint — summarization text only, never audio/ASR. See
`skills/prime-directive.md`.
