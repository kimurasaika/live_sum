import os

from dotenv import load_dotenv
from transformers import pipeline

load_dotenv()

_summarizer = None
_openrouter_client = None

MAX_CHUNK_CHARS = 2000


def get_summarizer():
    global _summarizer
    if _summarizer is None:
        _summarizer = pipeline(
            "summarization",
            model="csebuetnlp/mT5_multilingual_XLSum",
        )
    return _summarizer


def _get_openrouter_client():
    global _openrouter_client
    if _openrouter_client is None:
        from openai import OpenAI
        _openrouter_client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
        )
    return _openrouter_client


def _chunk_text(text: str, max_chars: int = MAX_CHUNK_CHARS) -> list[str]:
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)] or [text]


def _summarize_local(text: str) -> str:
    summarizer = get_summarizer()
    chunks = _chunk_text(text)
    summaries = []
    for chunk in chunks:
        if not chunk.strip():
            continue
        result = summarizer(chunk, max_length=150, min_length=20, do_sample=False)
        summaries.append(result[0]["summary_text"])
    return "\n\n".join(summaries)


def _summarize_openrouter(text: str) -> str:
    client = _get_openrouter_client()
    model = os.environ["OPENROUTER_MODEL"]
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"สรุปบทสนทนาต่อไปนี้เป็นภาษาไทยแบบกระชับ:\n\n{text}",
            }
        ],
    )
    return response.choices[0].message.content.strip()


def summarize_text(text: str) -> str:
    backend = os.getenv("SUMMARIZER_BACKEND", "local")
    if backend == "openrouter":
        return _summarize_openrouter(text)
    return _summarize_local(text)
