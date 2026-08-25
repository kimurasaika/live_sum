import json
from pathlib import Path

from gtts import gTTS

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data" / "testset"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SAMPLES = [
    {
        "text": "สวัสดีครับ วันนี้เราจะมาประชุมเรื่องงบประมาณของบริษัท",
        "keywords": ["สวัสดี", "ประชุม", "งบประมาณ", "บริษัท"],
    },
    {
        "text": "ทีมขายรายงานยอดขายเดือนนี้เพิ่มขึ้นสิบเปอร์เซ็นต์เมื่อเทียบกับเดือนที่แล้ว",
        "keywords": ["ทีมขาย", "ยอดขาย", "เปอร์เซ็นต์", "เดือน"],
    },
    {
        "text": "ฝ่ายบุคคลจะเปิดรับสมัครพนักงานใหม่สามตำแหน่งภายในสัปดาห์หน้า",
        "keywords": ["ฝ่ายบุคคล", "รับสมัคร", "พนักงาน", "ตำแหน่ง"],
    },
    {
        "text": "โครงการพัฒนาระบบจะเสร็จสิ้นภายในสิ้นเดือนธันวาคมตามแผนที่วางไว้",
        "keywords": ["โครงการ", "พัฒนาระบบ", "ธันวาคม", "แผน"],
    },
    {
        "text": "ลูกค้าต้องการให้เราส่งมอบสินค้าเร็วขึ้นกว่ากำหนดเดิมสองสัปดาห์",
        "keywords": ["ลูกค้า", "ส่งมอบ", "สินค้า", "กำหนด"],
    },
]


def main():
    manifest = []
    for i, sample in enumerate(SAMPLES):
        out_path = OUT_DIR / f"sample_{i}.mp3"
        if not out_path.exists():
            tts = gTTS(text=sample["text"], lang="th")
            tts.save(str(out_path))
        manifest.append({
            "file": out_path.name,
            "text": sample["text"],
            "keywords": sample["keywords"],
        })
        print(f"GENERATED: {out_path.name}")

    (OUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"MANIFEST: {OUT_DIR / 'manifest.json'}")


if __name__ == "__main__":
    main()
