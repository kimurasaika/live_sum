import io
import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS", "1")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from faster_whisper import WhisperModel
from pydub import AudioSegment

TESTSET_DIR = ROOT / "data" / "testset"
MANIFEST_PATH = TESTSET_DIR / "manifest.json"

CANDIDATES = [
    "Systran/faster-whisper-tiny",
    "Systran/faster-whisper-base",
    "Systran/faster-whisper-small",
    "Systran/faster-whisper-medium",
    "Systran/faster-whisper-large-v1",
    "Systran/faster-whisper-large-v2",
    "Systran/faster-whisper-large-v3",
    "Systran/faster-distil-whisper-large-v2",
    "Systran/faster-distil-whisper-large-v3",
    "deepdml/faster-whisper-large-v3-turbo-ct2",
    "Zoont/faster-whisper-large-v3-turbo-int8-ct2",
    "jootanehorror/faster-whisper-large-v3-turbo-ct2",
    "tbhrc/whisper_base_ct2",
    "jinlulululu/faster-whisper-small",
    "iadisirza-x/faster-whisper-thai-large-v3-ct2-prd-NEXT-Gen2",
    "iadisirza-x/whisper-thai-large-v3-adalora-prd-NEXT-ct2-Gen3",
    "iadisirza-x/whisper-thai-large-v3-adalora-prd-NEXT-ct2-Gen4",
    "nvidia/nemotron-3.5-asr-streaming-0.6b",
    "mesolitica/Malaysian-STT-Whisper",
    "mesolitica/Malaysian-STT-Whisper-Stage2",
    "typhoon-ai/typhoon-asr-realtime",
    "typhoon-ai/typhoon-asr-streaming-115m",
    "typhoon-ai/typhoon-asr-streaming-nemotron-0.6b",
]


def load_audio_pcm(path: Path) -> io.BytesIO:
    audio = AudioSegment.from_file(path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    pcm = io.BytesIO()
    audio.export(pcm, format="wav")
    pcm.seek(0)
    return pcm


def bench_one(repo_id: str, testset: list[dict]) -> dict:
    result = {"model": repo_id, "status": "OK"}
    try:
        t0 = time.perf_counter()
        model = WhisperModel(repo_id, device="cpu", compute_type="int8")
        t1 = time.perf_counter()
        result["load_s"] = round(t1 - t0, 2)

        total_transcribe_s = 0.0
        total_keywords = 0
        total_matched = 0
        per_sample = []

        for sample in testset:
            audio_path = TESTSET_DIR / sample["file"]
            pcm = load_audio_pcm(audio_path)

            t2 = time.perf_counter()
            segments, _ = model.transcribe(pcm, language="th", vad_filter=True)
            text = "".join(seg.text for seg in segments).strip()
            t3 = time.perf_counter()
            sample_time = t3 - t2
            total_transcribe_s += sample_time

            matched = [w for w in sample["keywords"] if w in text]
            total_keywords += len(sample["keywords"])
            total_matched += len(matched)

            per_sample.append({
                "file": sample["file"],
                "time_s": round(sample_time, 2),
                "matched": f"{len(matched)}/{len(sample['keywords'])}",
                "transcript": text,
            })

        result["transcribe_s_total"] = round(total_transcribe_s, 2)
        result["transcribe_s_avg"] = round(total_transcribe_s / len(testset), 2)
        result["accuracy"] = round(total_matched / total_keywords, 2)
        result["matched_total"] = f"{total_matched}/{total_keywords}"
        result["per_sample"] = per_sample
    except Exception as e:
        result["status"] = f"FAILED: {type(e).__name__}: {e}"
    return result


def main():
    testset = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    print(f"TESTSET_SIZE: {len(testset)} samples")

    results = []
    for repo_id in CANDIDATES:
        print(f"--- bench: {repo_id} ---")
        r = bench_one(repo_id, testset)
        for k, v in r.items():
            if k != "per_sample":
                print(f"  {k}: {v}")
        if r["status"] == "OK":
            for s in r["per_sample"]:
                print(f"    [{s['file']}] {s['time_s']}s matched={s['matched']} : {s['transcript']}")
        results.append(r)

    ok = [r for r in results if r["status"] == "OK"]
    ok.sort(key=lambda r: r["transcribe_s_total"])

    print("\n=== RESULTS (sorted by total transcribe time ascending) ===")
    print(f"{'model':<32}{'load_s':>8}{'total_s':>10}{'avg_s':>8}{'accuracy':>10}{'matched':>10}")
    for r in ok:
        print(f"{r['model']:<32}{r['load_s']:>8}{r['transcribe_s_total']:>10}{r['transcribe_s_avg']:>8}{r['accuracy']:>10}{r['matched_total']:>10}")

    failed = [r for r in results if r["status"] != "OK"]
    if failed:
        print("\n=== FAILED ===")
        for r in failed:
            print(f"{r['model']}: {r['status']}")

    sys.exit(0)


if __name__ == "__main__":
    main()
