import io
import os
import sys
import time
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

os.environ.setdefault("SUMMARIZER_BACKEND", "openrouter")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from backend.asr import transcribe_chunk
from backend.summarize import summarize_text

CLIP_PATH = ROOT / "data" / "clip.wav"
OUT_PATH = ROOT / "data" / "summary_30min.md"


def main():
    print("STEP 1: transcribing 30-min clip with Typhoon...")
    t0 = time.time()
    audio_bytes = CLIP_PATH.read_bytes()
    transcript = transcribe_chunk(audio_bytes)
    t1 = time.time()
    print(f"TRANSCRIBE_TIME: {t1 - t0:.1f}s")
    print(f"TRANSCRIPT_LENGTH: {len(transcript)} chars")

    print("STEP 2: summarizing via OpenRouter...")
    t2 = time.time()
    summary = summarize_text(transcript)
    t3 = time.time()
    print(f"SUMMARIZE_TIME: {t3 - t2:.1f}s")

    OUT_PATH.write_text(
        f"# 30-min Meeting Summary\n\n"
        f"Source: https://www.youtube.com/live/kSmdiXCeCdQ (segment 5155s - 6955s, 30 min)\n"
        f"Transcribed by: typhoon-ai/typhoon-asr-streaming-115m (NeMo)\n"
        f"Summarized by: OpenRouter ({os.getenv('OPENROUTER_MODEL')})\n"
        f"Transcribe time: {t1 - t0:.1f}s | Summarize time: {t3 - t2:.1f}s\n\n"
        f"## Summary\n\n{summary}\n\n"
        f"## Full Transcript\n\n{transcript}\n",
        encoding="utf-8",
    )
    print(f"WRITTEN: {OUT_PATH}")
    print(f"TOTAL_TIME: {t3 - t0:.1f}s")


if __name__ == "__main__":
    main()
