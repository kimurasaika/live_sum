import io
import os
import tempfile

os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS", "1")

from pydub import AudioSegment

_model = None

MODEL_ID = "typhoon-ai/typhoon-asr-streaming-115m"


def get_model():
    global _model
    if _model is None:
        from nemo.collections.asr.models import ASRModel
        _model = ASRModel.from_pretrained(model_name=MODEL_ID, map_location="cpu")
        _model.eval()
    return _model


def transcribe_chunk(audio_bytes: bytes) -> str:
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
    audio = audio.set_frame_rate(16000).set_channels(1)

    model = get_model()

    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp.close()
    try:
        audio.export(tmp.name, format="wav")
        result = model.transcribe([tmp.name])
        text = result[0].text if hasattr(result[0], "text") else str(result[0])
    finally:
        os.remove(tmp.name)

    return text.strip()
