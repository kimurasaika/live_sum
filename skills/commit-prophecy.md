# commit-prophecy

Git conventions for this project.

- Remote: `github.com/kimurasaika/live_sum`, branch `main`.
- Commit message: short summary line (what changed + why in one line), blank line, longer body
  only if the "why" isn't obvious from the diff alone.
- Never commit large/derived audio (`data/raw_audio.m4a`, `data/clip.wav`,
  `data/_bench_tmp.wav`) — see `.gitignore` and `vault-of-records.md`.
- Never commit `__pycache__/`, logs (`pipeline_out.log`, `pipeline_err.log`).
- Create new commits rather than amending, unless explicitly asked to amend.
- No `git push --force` to `main` without explicit confirmation.
