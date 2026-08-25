import asyncio
import io
import sys

import websockets

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


async def main():
    uri = "ws://127.0.0.1:8123/ws/asr"
    with open("test_sample_th.mp3", "rb") as f:
        audio_bytes = f.read()

    async with websockets.connect(uri) as ws:
        print("CONNECTED")
        await ws.send(audio_bytes)
        try:
            reply = await asyncio.wait_for(ws.recv(), timeout=60)
            print(f"RECEIVED: {reply}")
        except asyncio.TimeoutError:
            print("TIMEOUT: no reply within 60s")


asyncio.run(main())
