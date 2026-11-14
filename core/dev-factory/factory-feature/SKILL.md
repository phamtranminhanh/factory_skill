---
name: factory-feature
description: "Build new software behavior with a factory team, acceptance criteria, independent review and executable checks. Use for factory feature requests, not a diagnosis-only or review-only request."
---

# factory-feature

Run the shared Factory workflow with kind `feature`. Read [the common contract](../factory/SKILL.md), then [workflow](../factory/references/workflow.md), [agent roles](../factory/references/agents.md), and [evidence tooling](../factory/references/evidence.md). Do not route back to this wrapper; continue with the mode below. Use native Codex agents with fresh independent review, inheriting the current model unless the user chooses otherwise.

Define the observable behavior, compatibility constraints and explicit non-goals. Map each acceptance criterion to a test or independently inspected UI behavior. Read existing architecture before choosing new abstractions.

Use a planner for cross-surface changes; use separate researchers only for independent uncertainties. Allocate implementation by disjoint ownership, then integrate into one candidate. Review production wiring, state transitions, error paths and security boundaries affected by this feature.

Require the project's relevant tests/build/type checks and independent review. For UI changes, inspect the actual running interface at meaningful states and sizes through supported browser tools; a build alone is insufficient. A regression test that fails on the baseline is useful when the new behavior permits it, but feature mode does not fabricate a bug reproduction.

Finish with the working local change, or the PR when authorized. Do not add unrelated features or deployments.
