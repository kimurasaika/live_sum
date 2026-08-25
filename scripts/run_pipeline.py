import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.fetch_youtube_clip import fetch_clip
from backend.asr import transcribe_chunk
from backend.summarize import summarize_text

URL = "https://www.youtube.com/watch?v=kSmdiXCeCdQ"
START_SECONDS = 5155
DURATION_SECONDS = 600

DATA_DIR = ROOT / "data"
CLIP_PATH = DATA_DIR / "clip.wav"
README_PATH = ROOT / "README.md"


def main():
    if CLIP_PATH.exists():
        print(f"STEP 1: clip already exists, skipping fetch: {CLIP_PATH}")
    else:
        print("STEP 1: fetching clip...")
        fetch_clip(URL, START_SECONDS, DURATION_SECONDS, CLIP_PATH)
        print(f"CLIP_SAVED: {CLIP_PATH}")

    print("STEP 2: transcribing...")
    audio_bytes = CLIP_PATH.read_bytes()
    transcript = transcribe_chunk(audio_bytes)
    print(f"TRANSCRIPT_LENGTH: {len(transcript)}")

    print("STEP 3: summarizing...")
    summary = summarize_text(transcript)

    README_PATH.write_text(
        f"# Meeting Summary\n\n"
        f"Source: {URL} (segment {START_SECONDS}s - {START_SECONDS + DURATION_SECONDS}s)\n\n"
        f"## Summary\n\n{summary}\n\n"
        f"## Full Transcript\n\n{transcript}\n",
        encoding="utf-8",
    )
    print(f"README_WRITTEN: {README_PATH}")


if __name__ == "__main__":
    main()
