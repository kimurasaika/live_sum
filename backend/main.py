import asyncio
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.asr import transcribe_chunk

app = FastAPI()

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def index():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.websocket("/ws/asr")
async def asr_socket(websocket: WebSocket):
    await websocket.accept()
    loop = asyncio.get_running_loop()
    try:
        while True:
            audio_bytes = await websocket.receive_bytes()
            text = await loop.run_in_executor(None, transcribe_chunk, audio_bytes)
            if text:
                await websocket.send_text(text)
    except WebSocketDisconnect:
        pass
