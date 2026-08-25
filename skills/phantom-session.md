# phantom-session

Auth / Session / JWT. **Not applicable yet** — this project has no auth, no sessions, no login.
`/ws/asr` is open, localhost-only, no identity concept. Kept as a stub for future reference.

If auth ever gets added:
- [ ] Confirm it doesn't violate `prime-directive.md` (no cloud calls — self-hosted auth only,
  e.g. sessions/JWT signed locally, not a third-party auth provider)
- [ ] Decide what "session" even means here — single local user, or multi-user meeting rooms?
- [ ] Gate the WebSocket handshake, not just the HTTP routes
