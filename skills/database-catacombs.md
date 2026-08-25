# database-catacombs

Database. **Not applicable yet** — this project has no database. Transcripts/summaries are
written to flat files (`README.md`, `data/*.md`). Kept as a stub for future reference.

If a database ever gets added:
- [ ] Confirm it stays local (SQLite is the natural fit — no server process, no network,
  matches `prime-directive.md`'s offline rule better than Postgres/MySQL)
- [ ] Decide what needs persisting beyond flat files — meeting history? multiple transcripts?
  search across past summaries?
- [ ] Audio itself likely still belongs on disk, not in the DB — see `vault-of-records.md`
