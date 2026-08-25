# TASK.md — Current Task

## Task Name
Wire live summarization into the WebSocket ASR path

## What This Task Requires
1. `backend/main.py`: accumulate transcript fragments per connection; every
   `SUMMARIZE_EVERY_N_CHUNKS` non-empty transcript chunks, run `summarize_text()` on the
   full transcript-so-far and push it to the client as a distinct message type.
2. Switch the WS message protocol from plain text to JSON so client can tell transcript
   updates apart from summary updates: `{"type": "transcript", "text": ...}` /
   `{"type": "summary", "text": ...}`.
3. `summarize_text()` is CPU-bound (mT5) — must run via `run_in_executor`, same reasoning
   as the ASR blocking fix from the prior task. Do not reintroduce a blocking call.
4. `frontend/app.js` + `frontend/index.html`: parse the JSON messages, render transcript and
   summary in separate areas.

## Files In Scope
- backend/main.py
- frontend/app.js
- frontend/index.html

## Files Out Of Scope
- backend/asr.py, backend/summarize.py — reuse as-is, no changes to ASR/summarization logic
  itself, only how/when it's called from the live loop

## Acceptance Criteria
Script test (no browser available): a WS client sends >= `SUMMARIZE_EVERY_N_CHUNKS` real
audio chunks to `/ws/asr` and receives both message types back — at least one
`{"type":"transcript",...}` per chunk and at least one `{"type":"summary",...}` after the
Nth chunk, with non-empty `text` in both. Printed output is the verification proof.

## Approach
1. `main.py`: keep a `list[str]` of transcript fragments per connection (in-memory, scoped
   to the websocket handler's local closure — no cross-connection state).
2. Count non-empty transcript chunks; every Nth, join the accumulated fragments and call
   `summarize_text()` via executor, send result as a `summary` message.
3. Update `test_live_ws.py`-style test to send multiple chunks (reuse `test_sample_th.mp3`
   sent N times) and print every message received, distinguishing type.
4. Frontend: two divs (`#transcript`, `#summary`), `ws.onmessage` parses JSON and appends/
   replaces into the right one based on `msg.type`.

## Known Risks
- Summarizing a very short transcript (few chunks in) may hit mT5's `min_length=20` in a
  way that produces degenerate/short output — not fixing `summarize_text()`'s tuning in this
  task, just wiring; note the quality if it looks off in the verification run.
- Re-summarizing the *entire* transcript-so-far every N chunks (not just new text) means
  summarization cost grows with meeting length — acceptable for now, flag as a scaling
  concern for very long real meetings, not fixing here.
- `SUMMARIZE_EVERY_N_CHUNKS` is a guessed cadence (3) with no user-specified interval —
  reasonable default, easy to tune later, not asking the user to pick a number for a first
  pass.
