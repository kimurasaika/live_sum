# error-exorcism

Error handling / debugging patterns actually hit in this project. Full detail with exact error
text: `PROGRESS.md` Failed Attempts.

Recurring failure classes, so future debugging starts faster:

- **Windows HF cache symlink errors** (`OSError: [WinError 1314]`) — plain Windows accounts can't
  create the symlinks the HF hub cache wants. Fix: `HF_HUB_DISABLE_SYMLINKS=1` before any
  download. Doesn't cover every repo/file (some still fail) — if it recurs after setting this,
  it's a different file/repo hitting the same class, not a broken fix.
- **Wrong loader for model format.** `faster_whisper.WhisperModel` only loads CTranslate2 (ct2)
  checkpoints. Native transformers checkpoints (`pytorch_model.bin`/`model.bin` without ct2
  metadata) and NeMo checkpoints (`.nemo`) both fail with cryptic `Unable to open file 'model.bin'`
  errors if forced through `WhisperModel`. Check the repo's file format before picking a loader —
  this exact mistake caused multiple "model doesn't work" false negatives before the NeMo API
  fix (see `chronicle-of-changes.md`).
- **Unicode on Windows console.** `UnicodeEncodeError: 'charmap' codec can't encode characters`
  when printing Thai text. Fix: wrap stdout —
  `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")` — before any print of
  transcript/summary text.
- **Silent failure, not a crash.** The live WebSocket blocking bug (`iron-gate-backend.md`)
  doesn't throw — it just hangs until a keepalive ping timeout closes the connection with no
  traceback logged server-side. When something "just hangs" with no error, suspect a sync call
  blocking the event loop before assuming it's a network issue.

Rule: never retry a failed approach unchanged — the fix must address the actual root cause
found above, not just re-run the same call.
