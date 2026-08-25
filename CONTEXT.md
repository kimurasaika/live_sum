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
No modules exist yet. Each agent must add a module entry here when a new
module is created. Do not skip this step — the next agent depends on it.

Anticipated modules (not yet created):
- `backend/asr.py` — faster-whisper wrapper, streaming chunk transcription
- `backend/summarize.py` — transformers summarization pipeline wrapper
- `backend/main.py` — FastAPI app, WebSocket endpoint, static file serving
- `frontend/` — mic capture JS, WebSocket client, transcript/summary display

## Off-Limits Zones
No explicit off-limits zones beyond offline-only constraint. Defer to
AGENTS.md Hard Constraints.
