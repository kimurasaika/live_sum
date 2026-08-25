import asyncio
import io
import json
import sys

import websockets

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

N_CHUNKS = 3


async def main():
    uri = "ws://127.0.0.1:8123/ws/asr"
    with open("test_sample_th.mp3", "rb") as f:
        audio_bytes = f.read()

    got_transcript = False
    got_summary = False

    async with websockets.connect(uri) as ws:
        print("CONNECTED")
        for i in range(N_CHUNKS):
            await ws.send(audio_bytes)
            print(f"SENT chunk {i + 1}/{N_CHUNKS}")

        deadline_msgs = N_CHUNKS + 2
        for _ in range(deadline_msgs):
            try:
                raw = await asyncio.wait_for(ws.recv(), timeout=90)
            except asyncio.TimeoutError:
                print("TIMEOUT waiting for message")
                break
            msg = json.loads(raw)
            print(f"MSG type={msg['type']} text={msg['text']!r}")
            if msg["type"] == "transcript":
                got_transcript = True
            elif msg["type"] == "summary":
                got_summary = True
            if got_transcript and got_summary:
                break

    print(f"RESULT: got_transcript={got_transcript} got_summary={got_summary}")
    sys.exit(0 if (got_transcript and got_summary) else 1)


asyncio.run(main())
