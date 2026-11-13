---
name: factory-resume
description: "Resume a recorded Factory run after user feedback or a resolved blocker, preserving original criteria, candidate evidence and cumulative retry bounds."
---

# factory-resume

Read the common contract, workflow, agent roles and evidence references from `../factory/`. Locate the exact run the user means from the provided path or the target repository's Git common directory; if several are plausible, inspect titles/states and ask only if ambiguity remains. Never choose an unrelated project run.

Load state, plan, prior receipts, review and blocker. Compare current source/report fingerprints. Explain any changes made since the prior handoff; do not reuse stale passing evidence. Preserve original task kind and criteria unless the user explicitly changes them.

If there is a blocker, verify its resolution and record the answer with `resume`. An explicit user pause requires a resume request. Bounds span all resumes; a request to continue does not automatically authorize unlimited retries. Record any specifically authorized increase. Do not mutate state.json to bypass bounds.

Assign agents only for remaining work. Re-review corrected candidates independently. Finish with the actual requested deliverable and updated evidence, or another concrete blocker.
