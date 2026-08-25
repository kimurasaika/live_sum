# TASK.md — Current Task

## Task Name
Spike: integrate NeMo loader for Typhoon streaming ASR, verify if CPU realtime-capable

## What This Task Requires
1. Install `nemo_toolkit[asr]` (or minimal ASR-only extras) as one-time setup dependency.
2. Write `scripts/bench_typhoon_nemo.py` — loads `typhoon-ai/typhoon-asr-streaming-115m`
   (smallest streaming candidate) via NeMo API (not WhisperModel), on CPU.
3. Run transcribe on `test_sample_th.mp3`, measure: load time, transcribe wall-clock,
   matched-word count (same 4-word check as test_asr.py), RTF (transcribe_time / audio_duration).
4. Report only — do not touch backend/asr.py. This is a spike to answer: "can Typhoon
   streaming models even load+run via NeMo, and is CPU RTF < 1 (realtime-capable)?"

## Files In Scope
- scripts/bench_typhoon_nemo.py (create)
- requirements.txt (append nemo_toolkit, only if load succeeds and is worth keeping)

## Files Out Of Scope
- backend/asr.py, backend/main.py, frontend/*, backend/summarize.py

## Acceptance Criteria
`python scripts/bench_typhoon_nemo.py` exits 0, prints: load time, transcribe time,
audio duration, RTF, matched-word count (out of 4), PASS/FAIL vs >=3/4 threshold.
If load fails, exact error captured and logged to PROGRESS.md Failed Attempts —
that alone is an acceptable terminal outcome for this spike.

## Approach
1. pip install nemo_toolkit[asr] (heavy dependency, one-time network+disk, offline after).
2. Load model via `nemo.collections.asr.models.ASRModel.from_pretrained(...)` or
   equivalent HF-hosted NeMo checkpoint loader — check model card for exact loader API.
3. Preprocess audio same as backend/asr.py (16kHz mono wav).
4. Transcribe, time it, run same expected_words match logic as test_asr.py.

## Known Risks
- nemo_toolkit is a large, heavy dependency (torch + lightning + many extras) —
  install itself may take significant time/disk.
- Model card loader API unknown until inspected — may not be a simple one-liner.
- Prior attempts via WhisperModel failed outright; this is first real attempt via
  correct (NeMo) API — still no guarantee it loads or runs at usable speed on CPU.
- If nemo_toolkit conflicts with existing torch/faster-whisper install, may break env —
  test in isolation first if possible.
