import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)


def fetch_clip(url: str, start_seconds: int, duration_seconds: int, out_path: Path) -> Path:
    raw_audio = DATA_DIR / "raw_audio.m4a"

    subprocess.run(
        [
            "yt-dlp",
            "-x",
            "--audio-format", "m4a",
            "-o", str(raw_audio),
            url,
        ],
        check=True,
    )

    subprocess.run(
        [
            "ffmpeg", "-y",
            "-ss", str(start_seconds),
            "-t", str(duration_seconds),
            "-i", str(raw_audio),
            "-ar", "16000",
            "-ac", "1",
            str(out_path),
        ],
        check=True,
    )

    return out_path


if __name__ == "__main__":
    url = sys.argv[1]
    start = int(sys.argv[2])
    duration = int(sys.argv[3])
    out = DATA_DIR / "clip.wav"
    fetch_clip(url, start, duration, out)
    print(f"CLIP_SAVED: {out}")
