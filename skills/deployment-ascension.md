# deployment-ascension

Deploy: same scope as `skyforge-deployment.md` — see that file (local run instructions, HF
symlink caveat on Windows).

CI/CD: **not applicable yet.** No CI/CD pipeline exists in this project — single-machine,
manual `uvicorn` run only. If one gets added later, start here:
- [ ] Pick a runner (GitHub Actions is the default if hosted on GitHub, which this repo is:
  `github.com/kimurasaika/live_sum`)
- [ ] CPU-only test job running `python test_asr.py` — but note it needs the model cached or
  downloaded fresh (slow, ~GB-scale) — decide whether CI can afford that or should mock/skip ASR
- [ ] No deploy target exists yet (offline-first, local-only tool) — clarify with the user
  whether "deploy" ever means more than "hand someone the repo + `pip install`"
