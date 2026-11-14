---
name: factory-cifix
description: "Diagnose and repair a failed CI or build through a factory workflow, using the exact failing run, scoped changes, local reproduction and remote verification when available."
---

# factory-cifix

Run the shared Factory workflow with kind `ci_fix`. Read [the common contract](../factory/SKILL.md), then [workflow](../factory/references/workflow.md), [agent roles](../factory/references/agents.md), and [evidence tooling](../factory/references/evidence.md). Do not route back to this wrapper; continue with the mode below. Use native Codex agents with fresh independent review, inheriting the current model unless the user chooses otherwise.

Read the failed job, run URL/ID, head SHA, logs and workflow. First classify code failure, dependency/environment failure, flaky test, credential problem or infrastructure outage. A job that never reached tests is not a code regression.

Read delivery.md for connected CI access. Reproduce the relevant failing stage locally where feasible. An infrastructure fix may require only config; do not invent a test that cannot exercise it. Preserve the original failure artifact and show why the change addresses it.

Never disable required jobs, reduce test selection, relax assertions, skip failures or remove branch protection to obtain green. Dependency/version changes need evidence that they solve the observed failure.

Require independent review of workflow permissions, secret exposure, trigger behavior and affected commands. Verify the actual remote run on the fixed SHA when available and authorized. If remote validation is inaccessible, explicitly report locally verified / remote pending; do not call CI fixed solely from local success.
