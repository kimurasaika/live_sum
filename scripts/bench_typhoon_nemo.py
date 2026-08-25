import io
import os
import sys
import time

os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS", "1")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from pydub import AudioSegment

MODEL_ID = "typhoon-ai/typhoon-asr-streaming-115m"
AUDIO_PATH = sys.argv[1] if len(sys.argv) > 1 else "test_sample_th.mp3"
EXPECTED_WORDS = ["สวัสดี", "ประชุม", "งบประมาณ", "บริษัท"]


def preprocess(path):
    seg = AudioSegment.from_file(path).set_frame_rate(16000).set_channels(1)
    out_path = "data/_bench_tmp.wav"
    os.makedirs("data", exist_ok=True)
    seg.export(out_path, format="wav")
    return out_path, len(seg) / 1000.0


def main():
    wav_path, duration = preprocess(AUDIO_PATH)

    t0 = time.time()
    try:
        from nemo.collections.asr.models import ASRModel
        model = ASRModel.from_pretrained(model_name=MODEL_ID, map_location="cpu")
        model.eval()
    except Exception as e:
        print(f"MODEL: {MODEL_ID}")
        print(f"LOAD: FAILED — {type(e).__name__}: {e}")
        sys.exit(0)
    load_time = time.time() - t0

    t1 = time.time()
    try:
        result = model.transcribe([wav_path])
        text = result[0].text if hasattr(result[0], "text") else str(result[0])
    except Exception as e:
        print(f"MODEL: {MODEL_ID}")
        print(f"LOAD: OK ({load_time:.2f}s)")
        print(f"TRANSCRIBE: FAILED — {type(e).__name__}: {e}")
        sys.exit(0)
    transcribe_time = time.time() - t1

    matched = [w for w in EXPECTED_WORDS if w in text]
    rtf = transcribe_time / duration
    passed = len(matched) >= 3

    print(f"MODEL: {MODEL_ID}")
    print(f"LOAD_TIME: {load_time:.2f}s")
    print(f"AUDIO_DURATION: {duration:.2f}s")
    print(f"TRANSCRIBE_TIME: {transcribe_time:.2f}s")
    print(f"RTF: {rtf:.3f}")
    print(f"TRANSCRIPT: {text}")
    print(f"MATCHED: {matched} ({len(matched)}/4)")
    print(f"RESULT: {'PASS' if passed else 'FAIL'}")


if __name__ == "__main__":
    main()
