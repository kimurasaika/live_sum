# Meeting Summarizer (Thai, offline-first)

Local pipeline: Thai audio in (mic or file) → ASR transcript → local summarization. No cloud APIs, no telemetry, audio/transcripts never leave disk.

## Hard constraints
- Fully offline at runtime — no cloud ASR/LLM calls, no telemetry.
- Audio and transcripts stay on local disk.
- ASR runs on CPU, must support Thai, prioritizes accuracy + speed.
- Summarization via a local transformers pipeline (no server dependency, no Ollama).
- Live path: browser mic → WebSocket → backend ASR (no client-side ASR).
- Backend: Python + FastAPI.

## Structure
```
backend/     FastAPI server, asr.py (faster-whisper), summarize.py (mT5)
frontend/    minimal mic-capture UI (WebSocket client)
scripts/     benchmarking + one-off pipeline scripts
data/        test audio, benchmark testset, sample outputs
```

## Status (2026-08-25)

**Working:**
- ASR pipeline (backend + frontend) verified end-to-end — `python test_asr.py` passes with `large-v3` model.
- Full pipeline (YouTube clip → transcript → mT5 summary) runs and produces output — see `data/sample_pipeline_output.md` for a real run (quality caveat below).
- `uvicorn backend.main:app` boots clean.

**Known issue — model size vs. speed tradeoff, unresolved:**
`backend/asr.py` currently defaults to `faster-whisper` `"small"` (fast but weak accuracy) instead of the verified-accurate `large-v3` (too slow on real long audio: 30–56+ min for a 10-min clip on this CPU). Root cause not yet isolated — suspect `beam_size` (unset = default 5) rather than raw model size; not yet tested with `beam_size=1`.

**Promising alternative found — not yet integrated:**
`typhoon-ai/typhoon-asr-streaming-115m` (NeMo/RNNT architecture, loaded via `nemo.collections.asr.models.ASRModel`, not the Whisper API) benchmarks faster *and* more accurate than any faster-whisper size tried, on both a short clean sample and a real 10-minute noisy clip:

| Model | RTF (real 10-min clip) | Transcript quality |
|---|---|---|
| faster-whisper `medium` | 0.81 | weak — garbled on code-switched speech |
| faster-whisper `small` (current default) | — | weak — garbled, see `data/sample_pipeline_output.md` |
| `typhoon-asr-streaming-115m` (NeMo) | **0.372** | coherent, on-topic; one known repetition-loop artifact found |

Not yet wired into `backend/asr.py` — swapping engines means a different API (`ASRModel.transcribe()` vs `WhisperModel.transcribe()`) and a different approach for the live WebSocket mic path (NeMo RNNT has its own streaming/state-carry API vs. the current file-chunk transcription). Needs its own scoped task.

**Not yet tested:**
- Real browser mic → WebSocket flow (only backend pipeline + server boot verified directly, no browser automation run).

## Setup
```
pip install -r requirements.txt
python test_asr.py          # verify ASR path
uvicorn backend.main:app    # run server
```

Full history of what was tried, what failed and why, and open blockers: see `PROGRESS.md`. Current task scope: `TASK.md`. Hard rules and session protocol: `AGENTS.md`.
