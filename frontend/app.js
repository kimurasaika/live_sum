const startBtn = document.getElementById("start");
const stopBtn = document.getElementById("stop");
const transcriptDiv = document.getElementById("transcript");

let mediaRecorder;
let ws;

startBtn.onclick = async () => {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  ws = new WebSocket(`ws://${location.host}/ws/asr`);

  ws.onmessage = (event) => {
    transcriptDiv.textContent += event.data + " ";
  };

  ws.onopen = () => {
    mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm" });
    mediaRecorder.ondataavailable = async (e) => {
      if (e.data.size > 0 && ws.readyState === WebSocket.OPEN) {
        ws.send(await e.data.arrayBuffer());
      }
    };
    mediaRecorder.start(3000);
    startBtn.disabled = true;
    stopBtn.disabled = false;
  };
};

stopBtn.onclick = () => {
  mediaRecorder.stop();
  ws.close();
  startBtn.disabled = false;
  stopBtn.disabled = true;
};
