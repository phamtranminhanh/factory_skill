---
name: factory-refactor
description: "Restructure existing code through a factory workflow while preserving observable behavior, with characterization tests, controlled integration and independent review."
---

# factory-refactor

Run the shared Factory workflow with kind `refactor`. Read [the common contract](../factory/SKILL.md), then [workflow](../factory/references/workflow.md), [agent roles](../factory/references/agents.md), and [evidence tooling](../factory/references/evidence.md). Do not route back to this wrapper; continue with the mode below. Use native Codex agents with fresh independent review, inheriting the current model unless the user chooses otherwise.

State the structural objective and the behavior that must remain unchanged: API, data format, side effects, ordering, error semantics and performance constraints where relevant. Do not smuggle a new feature into a refactor.

Establish meaningful characterization checks before edits. Allocate independent modules to disjoint writers only when integration boundaries are clear. Prefer small transformations and keep public entry points wired.

Run unchanged tests and targeted compatibility checks, plus tamper detection. Test deletions or rewrites require independent evidence that behavior coverage remains adequate. A green suite after deleting the old assertions is insufficient.

Reviewer focuses on semantic drift, call-site updates, migration paths and complexity actually reduced. Deliver the structural result with exact checks and remaining risk.
