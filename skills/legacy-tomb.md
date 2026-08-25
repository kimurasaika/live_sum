# legacy-tomb

Legacy code handling. **Not applicable yet** — this project is young (single active
implementation, no deprecated versions carried forward). Kept as a stub for future reference.

If legacy code accumulates later (e.g. after the ASR engine swap discussed in
`chronicle-of-changes.md`):
- [ ] Delete outright rather than commenting out or feature-flagging — this is a small,
  single-maintainer project; dead code paths cost more to keep than to re-write later
- [ ] If keeping an old path temporarily for A/B comparison (e.g. faster-whisper vs. NeMo
  engine), say so explicitly in `chronicle-of-changes.md` with a removal condition, not just
  leave both wired in indefinitely
