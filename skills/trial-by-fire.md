# trial-by-fire

Testing and verification guide.

- `test_asr.py` — acceptance check for the ASR path. Transcribes `test_sample_th.mp3`, checks
  >=3 of 4 expected Thai words matched. Run: `python test_asr.py`.
- `scripts/bench_asr.py` — benchmarks candidate `faster-whisper`/ct2 models against
  `data/testset/` (5 samples), scores speed (RTF) + accuracy, ranks by min-max score.
- `scripts/bench_typhoon_nemo.py` — same idea, for NeMo-based Typhoon models. Takes an optional
  audio path arg (`python scripts/bench_typhoon_nemo.py data/clip.wav`) to test on real long audio
  instead of the short default sample.
- No test currently exercises the live WebSocket path end-to-end with a real browser — only
  direct backend calls have been verified. A manual `ws://.../ws/asr` client test surfaced the
  event-loop-blocking bug documented in `iron-gate-backend.md`.
- Verification standard: a task isn't done because it looks done — run the exact check, capture
  real output (not "tests passed"), and log it.
