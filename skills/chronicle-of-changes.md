# chronicle-of-changes

Condensed project history. Full detail with exact errors: `PROGRESS.md`.

- ASR pipeline (backend + frontend) built and verified with `large-v3` — passed accuracy check.
- Benchmarked 20+ `faster-whisper`/ct2 repos + 6 streaming-native repos on a 5-sample Thai
  testset. Winner among ct2 candidates: `Systran/faster-whisper-medium` (accuracy 0.70,
  RTF 0.81) — recommended but never applied to `backend/asr.py`.
- Full YouTube-clip → transcript → mT5 summary pipeline run once on a real 10-min clip.
  `backend/asr.py` had to be downgraded `large-v3` → `medium` → `small` purely for speed on this
  CPU — quality suffered (garbled transcript on code-switched casual speech).
- Spike: loaded `typhoon-ai/typhoon-asr-streaming-115m` via the correct NeMo API (prior attempts
  failed because they used the wrong loader, `WhisperModel`, on a NeMo-format model). Result:
  **fastest and most accurate ASR found in this project** — RTF 0.372 on the real 10-min clip
  (vs 0.81 for `medium`), coherent transcript, one known repetition-loop defect. Not yet wired
  into `backend/asr.py` — different API, needs its own scoped integration.
- Repo pushed to `github.com/kimurasaika/live_sum`.
- Live-use test (real WebSocket call): confirmed the event-loop-blocking bug in
  `iron-gate-backend.md` and confirmed live summarization was never implemented — the live path
  currently only streams raw transcript fragments, no summary, and can die mid-transcription.

Current open items: fix the blocking bug, decide whether/how to wire summarization into the live
loop, decide whether to integrate the Typhoon/NeMo ASR engine as the new default.
