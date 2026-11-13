---
name: factory-testgap
description: "Add missing regression or behavior coverage through a factory workflow, independently reviewing test sensitivity and preserving production behavior."
---

# factory-testgap

Run the shared Factory workflow with kind `test_gap`. Read [the common contract](../factory/SKILL.md), then [workflow](../factory/references/workflow.md), [agent roles](../factory/references/agents.md), and [evidence tooling](../factory/references/evidence.md). Do not route back to this wrapper; continue with the mode below. Use native Codex agents with fresh independent review, inheriting the current model unless the user chooses otherwise.

Identify uncovered behavior and the relevant public entry point. Prioritize risk and boundary cases rather than a coverage percentage target. Read the current suite and avoid duplicating existing assertions.

Keep production behavior unchanged unless the user authorizes a discovered bugfix. Test infrastructure adjustments must be justified. If a new test exposes a product bug, report it and establish whether fixing it is in scope; do not bless the wrong behavior to make the test green.

Demonstrate sensitivity where feasible: a targeted mutation, baseline variant or known incorrect input should make the test fail. Restore any experimental mutation before final verification and refresh the candidate fingerprint. Tamper detection and independent review still apply even though the main output is tests.

Run the new tests and the relevant existing suite; explain what cases remain uncovered. Do not promise that a passing percentage establishes correctness.
