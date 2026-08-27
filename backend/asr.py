import io
import os
import tempfile

os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS", "1")

from pydub import AudioSegment

_model = None

MODEL_ID = "typhoon-ai/typhoon-asr-streaming-115m"

# Conformer self-attention memory scales O(n^2) with input length. A whole
# unchunked file OOMs past ~15-18 min on this machine's RAM (verified: 10 min
# ok, 30 min tried to allocate ~32GB). Slice anything longer than this before
# calling NeMo transcribe, same discipline the live WS path already uses.
CHUNK_MS = 20_000


def get_model():
    global _model
    if _model is None:
        from nemo.collections.asr.models import ASRModel
        _model = ASRModel.from_pretrained(model_name=MODEL_ID, map_location="cpu")
        _model.eval()
    return _model


def _transcribe_wav_file(model, audio: AudioSegment) -> str:
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp.close()
    try:
        audio.export(tmp.name, format="wav")
        result = model.transcribe([tmp.name])
        text = result[0].text if hasattr(result[0], "text") else str(result[0])
    finally:
        os.remove(tmp.name)
    return text.strip()


def transcribe_chunk(audio_bytes: bytes) -> str:
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
    audio = audio.set_frame_rate(16000).set_channels(1)

    model = get_model()

    if len(audio) <= CHUNK_MS:
        return _transcribe_wav_file(model, audio)

    pieces = [audio[i:i + CHUNK_MS] for i in range(0, len(audio), CHUNK_MS)]
    texts = [_transcribe_wav_file(model, piece) for piece in pieces]
    return " ".join(t for t in texts if t)
