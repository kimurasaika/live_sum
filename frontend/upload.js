const fileInput = document.getElementById("file");
const submitBtn = document.getElementById("submit");
const statusEl = document.getElementById("status");
const transcriptDiv = document.getElementById("transcript");
const summaryDiv = document.getElementById("summary");

submitBtn.onclick = async () => {
  const file = fileInput.files[0];
  if (!file) {
    statusEl.textContent = "กรุณาเลือกไฟล์ก่อน";
    return;
  }

  submitBtn.disabled = true;
  statusEl.textContent = "กำลังถอดเสียงและสรุป... (ไฟล์ยาวอาจใช้เวลาหลายนาที)";
  transcriptDiv.textContent = "";
  transcriptDiv.classList.add("empty");
  summaryDiv.textContent = "";
  summaryDiv.classList.add("empty");

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("/api/upload", { method: "POST", body: formData });
    if (!res.ok) {
      throw new Error(`server error: ${res.status}`);
    }
    const data = await res.json();
    transcriptDiv.textContent = data.transcript || "(ว่าง)";
    transcriptDiv.classList.remove("empty");
    summaryDiv.textContent = data.summary || "(ว่าง)";
    summaryDiv.classList.remove("empty");
    statusEl.textContent = "เสร็จสิ้น";
  } catch (err) {
    statusEl.textContent = `เกิดข้อผิดพลาด: ${err.message}`;
  } finally {
    submitBtn.disabled = false;
  }
};
