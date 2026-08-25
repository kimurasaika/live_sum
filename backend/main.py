import asyncio
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.asr import get_model, transcribe_chunk
from backend.summarize import get_summarizer, summarize_text

app = FastAPI()

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

SUMMARIZE_EVERY_N_CHUNKS = 3
SUMMARY_WINDOW_CHUNKS = 10


@app.on_event("startup")
def warm_up_models():
    # Load + JIT-warm both models on the main thread at boot. NeMo's first
    # transcribe triggers numba JIT compilation; doing that lazily inside a
    # run_in_executor worker thread deadlocks on Windows (observed: process
    # goes idle, CPU flat, no exception, connection eventually times out).
    get_model()
    sample_path = Path(__file__).resolve().parent.parent / "test_sample_th.mp3"
    if sample_path.exists():
        transcribe_chunk(sample_path.read_bytes())
    get_summarizer()


@app.get("/")
def index():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.websocket("/ws/asr")
async def asr_socket(websocket: WebSocket):
    await websocket.accept()
    loop = asyncio.get_running_loop()
    transcript_parts: list[str] = []
    chunks_since_summary = 0
    try:
        while True:
            audio_bytes = await websocket.receive_bytes()
            text = await loop.run_in_executor(None, transcribe_chunk, audio_bytes)
            if not text:
                continue

            transcript_parts.append(text)
            await websocket.send_json({"type": "transcript", "text": text})

            chunks_since_summary += 1
            if chunks_since_summary >= SUMMARIZE_EVERY_N_CHUNKS:
                chunks_since_summary = 0
                # Rolling window, not the ever-growing full transcript: summarizing
                # everything-so-far makes each call slower as the meeting goes on,
                # and the CPU-bound work (even off the event loop thread) starves
                # the loop of GIL time long enough to blow the WS ping timeout on
                # real long-running streams (observed past ~75 chunks / ~4 min in).
                window_text = " ".join(transcript_parts[-SUMMARY_WINDOW_CHUNKS:])
                summary = await loop.run_in_executor(None, summarize_text, window_text)
                await websocket.send_json({"type": "summary", "text": summary})
    except WebSocketDisconnect:
        pass
