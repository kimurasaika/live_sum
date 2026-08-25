# observability-eye

Logging, metrics, monitoring. **Not applicable yet** — this project only has ad-hoc `print()`
output and `uvicorn`'s default request logs. No structured logging, no metrics, no monitoring
stack. Kept as a stub for future reference.

If observability gets added later:
- [ ] Confirm any metrics/logging backend stays local (no hosted APM/telemetry — violates
  `prime-directive.md`'s no-telemetry rule; local log files or a local Prometheus are fine)
- [ ] Start with structured logging around the two things that matter most for this project:
  ASR transcribe time (for RTF tracking, see `chronicle-of-changes.md` benchmark history) and
  the live WebSocket connection lifecycle (to catch the blocking-bug class documented in
  `iron-gate-backend.md` earlier next time)
