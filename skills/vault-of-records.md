# vault-of-records

Data and storage conventions. Directory: `data/`.

- `data/testset/` — small gTTS-generated Thai benchmark set (5 samples, `manifest.json`) used by
  `scripts/bench_asr.py`. Safe to commit (small, synthetic, no real user audio).
- `data/clip.wav`, `data/raw_audio.m4a`, `data/_bench_tmp.wav` — large real/derived audio
  (tens–hundreds of MB). **Never commit these** — covered by `.gitignore`. Regenerate via
  `scripts/fetch_youtube_clip.py` when needed.
- `data/sample_pipeline_output.md` — a real (imperfect) pipeline run kept as a reference sample,
  not the project README.
- Root-level `test_sample.wav` / `test_sample_th.mp3` — small fixed test clips used by
  `test_asr.py`. Keep committed; they're the acceptance-check fixtures.
- Rule of thumb: if it's synthetic/small/needed for a test to run standalone, commit it. If it's
  a large real recording, keep it local-only and regeneratable by script.
