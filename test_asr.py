import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent))

from backend.asr import transcribe_chunk

sample_path = Path(__file__).resolve().parent / "test_sample_th.mp3"
audio_bytes = sample_path.read_bytes()

expected_words = ["สวัสดี", "ประชุม", "งบประมาณ", "บริษัท"]

text = transcribe_chunk(audio_bytes)
print(f"TRANSCRIPT: {text!r}")

matched = [w for w in expected_words if w in text]
print(f"MATCHED: {matched}")

if len(matched) < len(expected_words) // 2 + 1:
    print("FAIL: transcript does not sufficiently match expected Thai sentence")
    sys.exit(1)

print("PASS: transcript matches expected Thai sentence")
sys.exit(0)
