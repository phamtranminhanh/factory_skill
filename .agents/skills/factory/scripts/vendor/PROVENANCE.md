# Vendored test-tamper detector

`tamper_guard.py` is copied unchanged from:

- Repository: https://github.com/no-human-ai/no_human
- Commit: `cdcbd0af086890eb4ecdbece1c1ca8dc168e5907`
- Path: `src/no_human/testing/tamper_guard.py`
- License: MIT; full notice retained in `LICENSE.no_human`.

It has only standard-library dependencies. The Factory helper supplies its own
NUL-separated Git snapshot collection and does not import the no_human runtime.
Updates must preserve license notices, compare upstream changes, and rerun the
behavioral regression checks before replacing the vendored copy.
