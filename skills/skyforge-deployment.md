# skyforge-deployment

Run/deploy guide. Local-only — there is no hosted deployment target (offline-by-design, see
`prime-directive.md`).

```
pip install -r requirements.txt
python test_asr.py                 # verify ASR path before relying on it
python -m uvicorn backend.main:app --port 8000
```

- First run downloads models to the local HF cache (one-time network exception). On Windows,
  set `HF_HUB_DISABLE_SYMLINKS=1` before downloading — plain Windows accounts can't create the
  symlinks the HF hub cache normally uses (`WinError 1314`).
- No containerization, no CI/CD pipeline exists yet — single-machine, single-process only.
- Batch pipeline (`scripts/run_pipeline.py`, `scripts/_summarize_typhoon_clip.py`) is invoked
  manually, not a server route.
