import io
from faster_whisper import WhisperModel
from pydub import AudioSegment

_model: WhisperModel | None = None


def get_model() -> WhisperModel:
    global _model
    if _model is None:
        _model = WhisperModel("small", device="cpu", compute_type="int8")
    return _model


def transcribe_chunk(audio_bytes: bytes) -> str:
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
    audio = audio.set_frame_rate(16000).set_channels(1)
    pcm = io.BytesIO()
    audio.export(pcm, format="wav")
    pcm.seek(0)

    model = get_model()
    segments, _ = model.transcribe(pcm, language="th", vad_filter=True)
    return "".join(segment.text for segment in segments).strip()
