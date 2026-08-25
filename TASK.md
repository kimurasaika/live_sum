# TASK.md — Current Task

## Task Name
Fix batch/long-audio OOM — chunk audio before NeMo transcribe (same pattern as live path)

## What This Task Requires
`transcribe_chunk()` in `backend/asr.py` currently passes whole audio files straight to NeMo's
`model.transcribe()`. Works fine up to ~10 min; OOMs (~32GB alloc attempt) around 30 min because
Conformer self-attention memory scales O(n²) with audio length. Estimated real ceiling on this
machine (16.7GB RAM): ~15-18 min for a single unchunked call — see PROGRESS.md for the math.

The live WebSocket path already avoids this (chunks audio into 3s pieces client-side before
each `transcribe_chunk()` call, verified stable through a 200-chunk/~10-min continuous real
stream). This task ports that same chunking discipline into the *batch* path, so a single long
audio file (30 min–3 hr) can be transcribed without OOM.

1. Add audio-chunking logic reusable by both `backend/asr.py` batch calls and any future batch
   script — split a long `AudioSegment` into fixed-size pieces (e.g. 20-30s, tune based on
   real memory headroom) before calling NeMo `transcribe()` per piece, then join the transcripts.
2. Decide where this lives: either inside `transcribe_chunk()` itself (auto-chunk if input
   audio exceeds some duration threshold), or as a separate `transcribe_long_audio()` function
   so the live per-chunk path (already small, always <10s) stays untouched and simple.
3. Re-run `scripts/test_30min_pipeline.py` (already exists, was the repro case) — should
   complete without OOM once fixed.

## Files In Scope
- backend/asr.py
- scripts/test_30min_pipeline.py (re-run only, not necessarily edited)

## Files Out Of Scope
- backend/main.py — live WebSocket path already chunks correctly client-side, don't touch
- backend/summarize.py — summarization isn't the bottleneck here, already handles long text
  via its own 2000-char chunking

## Acceptance Criteria
`python scripts/test_30min_pipeline.py` exits 0, writes `data/summary_30min.md`, no
`RuntimeError`/`MemoryError`. Report TRANSCRIBE_TIME and transcript length as proof — compare
against the 10-min baseline (223s transcribe, RTF 0.372) to sanity-check the chunked approach
didn't tank speed.

## Approach
1. Write a chunking helper (pydub `AudioSegment` slicing, same technique already used in
   `scripts/test_live_stream_real_clip.py`'s `chunk_audio()` — can likely reuse/adapt that).
2. Wire it into `backend/asr.py` for inputs over a duration threshold (~60s, tune after testing).
3. Join per-chunk transcripts with spaces (same as the live path's `" ".join(transcript_parts)`).
4. Test on the existing `data/clip.wav` (currently the 30-min segment from the OOM repro).

## Known Risks
- Chunk boundary cuts mid-word/mid-sentence — transcript quality may degrade slightly at chunk
  edges compared to a single unchunked pass (which itself only worked up to ~10 min anyway, so
  no regression vs. a working baseline — just a new tradeoff to be aware of).
- Chunk size is a speed/memory tradeoff — smaller chunks are safer but add more per-chunk
  overhead (model call setup cost seen earlier, ~tenths of a second per call); needs empirical
  tuning, not a guessed constant trusted blindly.
- `data/clip.wav` right now holds the 30-min segment (overwrote the earlier 10-min one) — reuse
  it for this test rather than re-fetching, to save a yt-dlp round-trip.
