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
backend/     FastAPI server, asr.py (Typhoon NeMo ASR), summarize.py (mT5 local / OpenRouter cloud)
frontend/    index.html (landing), asr.html+app.js (realtime), upload.html+upload.js (file mode)
scripts/     benchmarking + one-off pipeline scripts
data/        test audio, benchmark testset, sample outputs
```

## Usage — two modes

| Route | Mode | Flow |
|---|---|---|
| `/` | Landing | Pick a mode |
| `/asr` | Realtime | Browser mic → WebSocket → live transcript + rolling summary |
| `/upload` | File upload | Pick an audio file → POST `/api/upload` → full transcript + one summary |

## Run with Docker

```
git clone git@github.com:kimurasaika/live_sum.git
cd live_sum
docker build -t meeting-sum .
docker run -p 8080:8080 --env-file .env meeting-sum
```

Open `http://localhost:8080`.

Notes:
- First container start downloads the ASR (Typhoon NeMo) and summarization (mT5) models —
  needs network once, same as local dev. Model load + JIT warm-up adds ~2-3 min to the first
  boot (see `backend/main.py` `warm_up_models`). To avoid re-downloading on every container
  recreation, mount a volume for the HF cache, e.g. add `-v meeting-sum-hf-cache:/root/.cache/huggingface`
  to the `docker run` command.
- `--env-file .env` is only needed if using the OpenRouter cloud summarization backend
  (`SUMMARIZER_BACKEND=openrouter`, see `.env.example`). Default (`local`) needs no env file.
- Runtime itself makes no outbound calls beyond that one-time model download and the optional
  OpenRouter summarize call — audio never leaves the container either way.

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

## Skills

Domain guides in `skills/`, one file per concern:

| File | Covers |
|---|---|
| `prime-directive.md` | Hard constraints (offline-only, local storage, CPU ASR, no client-side ASR) |
| `iron-gate-backend.md` | FastAPI backend — routes, WebSocket handler, known blocking bug |
| `neon-forge-frontend.md` | Mic-capture UI — flow, chunking, current gaps |
| `aegis-ward.md` | Security / offline-safety rules |
| `vault-of-records.md` | Data/storage conventions — what's committed vs. local-only |
| `trial-by-fire.md` | Testing and verification — acceptance checks, benchmark scripts |
| `chronicle-of-changes.md` | Condensed project history |
| `skyforge-deployment.md` | Run/deploy instructions |
| `quantum-frontend.md` | Frontend (alias of `neon-forge-frontend.md`) |
| `abyssal-api.md` | Backend/API (alias of `iron-gate-backend.md`) |
| `cipher-sanctum.md` | Security (alias of `aegis-ward.md`) |
| `test-chamber.md` | Testing (alias of `trial-by-fire.md`) |
| `deployment-ascension.md` | CI/CD (stub — none exists yet) + deploy (alias of `skyforge-deployment.md`) |
| `error-exorcism.md` | Recurring error patterns and how they were actually fixed |
| `commit-prophecy.md` | Git conventions |
| `phantom-session.md` | Auth/Session/JWT — stub, not applicable yet |
| `database-catacombs.md` | Database — stub, not applicable yet |
| `migration-rites.md` | DB migrations — stub, not applicable yet |
| `cache-dimension.md` | Redis/cache — stub, not applicable yet |
| `observability-eye.md` | Logging/metrics/monitoring — stub, not applicable yet |
| `mcp-portal.md` | MCP integration — stub, not applicable yet |
| `prompt-firewall.md` | Prompt injection defense — stub, low relevance currently |
| `legacy-tomb.md` | Legacy code handling — stub, not applicable yet |
