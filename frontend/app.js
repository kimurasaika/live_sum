const startBtn = document.getElementById("start");
const stopBtn = document.getElementById("stop");
const statusEl = document.getElementById("status");
const transcriptDiv = document.getElementById("transcript");
const summaryDiv = document.getElementById("summary");

let mediaRecorder;
let ws;

startBtn.onclick = async () => {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  ws = new WebSocket(`ws://${location.host}/ws/asr`);

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.type === "transcript") {
      transcriptDiv.textContent += msg.text + " ";
      transcriptDiv.classList.remove("empty");
    } else if (msg.type === "summary") {
      summaryDiv.textContent = msg.text;
      summaryDiv.classList.remove("empty");
    }
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
    statusEl.textContent = "กำลังบันทึก...";
  };
};

stopBtn.onclick = () => {
  mediaRecorder.stop();
  ws.close();
  startBtn.disabled = false;
  stopBtn.disabled = true;
  statusEl.textContent = "หยุดแล้ว";
};
