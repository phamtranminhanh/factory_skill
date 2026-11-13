---
name: factory-pr
description: "Hand off a locally verified Factory change as an authorized pull request or merge request, checking evidence freshness, commit identity and remote delivery."
---

# factory-pr

Read `../factory/SKILL.md`, the shared evidence reference and `../factory/references/delivery.md`. This wrapper publishes a requested PR/MR; it does not independently authorize merge or deploy.

Find the existing run and check current candidate against all recorded proofs. If no evidence run exists, establish the actual task criteria and baseline, then run the appropriate verification/review workflow; do not manufacture passing receipts for an already-written diff.

Inspect all changes and preserve unrelated user work. Commit the exact verified candidate as appropriate, rerun the gate after hooks, and confirm the intended remote/base. Create or update the intended PR through available forge tools/CLI using a body file or structured argument.

Verify returned URL and remote head SHA against the delivered commit. Report exact local/remote checks and any pending CI. Missing forge access is a concrete delivery blocker with the local change intact. Do not copy secrets or internal raw logs into the PR.
