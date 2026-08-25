# cache-dimension

Redis / cache. **Not applicable yet** — no cache layer exists. The only "cache" in this project
is the Hugging Face model cache (local disk, not Redis) — see `skyforge-deployment.md`. Kept as
a stub for future reference.

If a cache layer ever gets added:
- [ ] Confirm it runs locally (no hosted Redis — violates `prime-directive.md`'s offline rule)
- [ ] Question the need first — this is a single-process, single-user local tool; a cache adds
  an operational dependency (a Redis process to run/manage) that may not pay for itself here
