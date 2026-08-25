# neon-forge-frontend

Minimal mic-capture UI. Files: `frontend/index.html`, `frontend/app.js`.

- No build step, no framework — plain HTML + vanilla JS, served directly by FastAPI's
  `StaticFiles` mount.
- Flow: `Start` → `getUserMedia({audio:true})` → open WebSocket to `/ws/asr` → `MediaRecorder`
  captures `audio/webm` chunks every 3s (`mediaRecorder.start(3000)`) → each chunk sent as raw
  bytes over the socket → incoming text appended to `#transcript` div.
- `Stop` stops the recorder and closes the socket.
- No summary display anywhere in the UI — matches the backend gap in `iron-gate-backend.md`
  (live summarization isn't wired up yet, so there's nothing for the frontend to show).
- Untested against a real browser session (no browser automation run yet) — only the backend
  WebSocket handler has been exercised directly.
