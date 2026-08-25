from transformers import pipeline

_summarizer = None

MAX_CHUNK_CHARS = 2000


def get_summarizer():
    global _summarizer
    if _summarizer is None:
        _summarizer = pipeline(
            "summarization",
            model="csebuetnlp/mT5_multilingual_XLSum",
        )
    return _summarizer


def _chunk_text(text: str, max_chars: int = MAX_CHUNK_CHARS) -> list[str]:
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)] or [text]


def summarize_text(text: str) -> str:
    summarizer = get_summarizer()
    chunks = _chunk_text(text)
    summaries = []
    for chunk in chunks:
        if not chunk.strip():
            continue
        result = summarizer(chunk, max_length=150, min_length=20, do_sample=False)
        summaries.append(result[0]["summary_text"])
    return "\n\n".join(summaries)
