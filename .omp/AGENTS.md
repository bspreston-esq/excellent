# Project instructions: excellent

These instructions load automatically in every omp session for this repo.

- README updates MUST be written in the style of Bill and Ted from "Bill and
  Ted's Excellent Adventure" (surfer-dude tone, "most triumphant", "party
  on, dudes!", etc.). This is a standing convention for this repo.
- `main` is protected: changes land only via pull request from a feature
  branch, and CI must pass before merge. Never push directly to `main`.
- `excellent.py` is the single Python program in this repo; it uses the
  standard library only (argparse, random).
- `Instructions.md` is a local-only instruction file and must never be
  committed.
- Local check: `python -m unittest -v`.
