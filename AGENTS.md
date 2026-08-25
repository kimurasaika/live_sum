# AGENTS.md — Project Rulebook

## Session Start Protocol
Every agent, every session, must complete these steps before touching any file:
1. Read this file completely.
2. Read PROGRESS.md — understand what is done and what has failed.
3. Read TASK.md — understand the current task and its acceptance criteria.
4. Read CONTEXT.md only if the current task touches the modules listed there.
5. Do not write any code until steps 1–4 are complete.
6. Apply these operating principles before writing any code:
   - Infer maximum from context before asking anything.
   - Never touch files outside TASK.md Files In Scope.
   - Plan the complete implementation path before the first line of code.
   - A task is not done until acceptance criteria passes a concrete check.
   - Log every failure with exact error. Never retry a failed approach unchanged.

## Hard Constraints
- Fully offline. No external network calls anywhere in the runtime path (no cloud ASR/LLM APIs, no telemetry).
- Audio and transcripts never leave local disk. No cloud storage, no third-party upload.
- ASR must run on CPU, must support Thai language, must prioritize accuracy and speed.
- Summarization runs on a local transformers pipeline — no server dependency (no Ollama).
- Live transcription path: browser mic → WebSocket → backend ASR. No client-side ASR.
- Python + FastAPI backend. Do not introduce a second backend framework.

## Code Style Rules
Infer conventions from existing code patterns. Match what is already there.
Do not introduce new patterns without flagging them in PROGRESS.md first.

## File Update Protocol
- AGENTS.md  → Never updated mid-project. Only the human changes this file.
- PROGRESS.md → Updated after every completed task and every failed attempt.
- TASK.md    → Completely overwritten when a new task begins. Never appended to.
- CONTEXT.md → Updated only when architecture meaningfully changes: new modules,
               deleted modules, changed interfaces. Not for minor utility files.

## Off-Limits
Defer to Hard Constraints above for all restrictions.
