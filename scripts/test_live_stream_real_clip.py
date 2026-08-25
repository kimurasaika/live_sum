import asyncio
import io
import json
import sys
from pathlib import Path

import websockets
from pydub import AudioSegment

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
CLIP_PATH = ROOT / "data" / "clip.wav"
CHUNK_MS = 3000


def chunk_audio(path: Path, chunk_ms: int):
    audio = AudioSegment.from_file(path)
    chunks = []
    for start in range(0, len(audio), chunk_ms):
        piece = audio[start:start + chunk_ms]
        buf = io.BytesIO()
        piece.export(buf, format="wav")
        chunks.append(buf.getvalue())
    return chunks


async def main():
    if not CLIP_PATH.exists():
        print(f"MISSING: {CLIP_PATH}")
        sys.exit(1)

    print("STEP: chunking clip.wav into 3s pieces...")
    chunks = chunk_audio(CLIP_PATH, CHUNK_MS)
    print(f"CHUNKS: {len(chunks)} pieces, {CHUNK_MS/1000:.0f}s each")

    uri = "ws://127.0.0.1:8123/ws/asr"
    transcripts = []
    summaries = []

    async with websockets.connect(uri, ping_timeout=None) as ws:
        print("CONNECTED")

        async def sender():
            for i, chunk in enumerate(chunks):
                await ws.send(chunk)
                print(f"SENT chunk {i + 1}/{len(chunks)}")
                await asyncio.sleep(0.05)

        async def receiver():
            while True:
                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=120)
                except asyncio.TimeoutError:
                    print("RECEIVER TIMEOUT — no message in 120s, stopping")
                    return
                msg = json.loads(raw)
                if msg["type"] == "transcript":
                    transcripts.append(msg["text"])
                    print(f"[TRANSCRIPT] {msg['text']}")
                elif msg["type"] == "summary":
                    summaries.append(msg["text"])
                    print(f"[SUMMARY]    {msg['text']}")

        send_task = asyncio.create_task(sender())
        recv_task = asyncio.create_task(receiver())
        await send_task
        print("ALL CHUNKS SENT — waiting for server to drain remaining replies...")
        await recv_task

    print(f"\nTOTAL_TRANSCRIPT_MSGS: {len(transcripts)}")
    print(f"TOTAL_SUMMARY_MSGS: {len(summaries)}")
    full_transcript = " ".join(transcripts)
    print(f"FULL_TRANSCRIPT_LENGTH: {len(full_transcript)}")
    if summaries:
        print(f"LAST_SUMMARY: {summaries[-1]}")

    out_path = ROOT / "data" / "live_simulation_result.md"
    out_path.write_text(
        f"# Live simulation result (chunked real 10-min clip)\n\n"
        f"Chunks sent: {len(chunks)} x {CHUNK_MS/1000:.0f}s\n"
        f"Transcript messages received: {len(transcripts)}\n"
        f"Summary messages received: {len(summaries)}\n\n"
        f"## Full transcript (concatenated)\n\n{full_transcript}\n\n"
        f"## Summaries over time\n\n" + "\n\n---\n\n".join(summaries),
        encoding="utf-8",
    )
    print(f"WRITTEN: {out_path}")


asyncio.run(main())
