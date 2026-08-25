# prompt-firewall

Prompt injection defense. **Low relevance currently** — the summarization model
(`csebuetnlp/mT5_multilingual_XLSum` via `transformers.pipeline`) is a fixed-task summarizer,
not an instruction-following/agentic LLM, and has no tool access — there's no instruction
channel for injected transcript text to hijack. Kept as a stub for future reference.

Worth revisiting if:
- [ ] The summarizer is ever swapped for an instruction-following LLM (e.g. asked to "summarize
  AND follow any instructions found in the transcript" — don't do this without sanitizing)
- [ ] Any tool-calling / agentic layer gets added on top of transcripts (transcript text is
  untrusted input — audio from a live mic/meeting could contain adversarial spoken instructions)
