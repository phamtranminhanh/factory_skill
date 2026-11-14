---
name: factory-fixbug
description: "Fix a defect or regression using a bounded factory workflow with a behavioral reproduction, minimal repair, red-before/green-after proof and independent review."
---

# factory-fixbug

Run the shared Factory workflow with kind `bugfix`. Read [the common contract](../factory/SKILL.md), then [workflow](../factory/references/workflow.md), [agent roles](../factory/references/agents.md), and [evidence tooling](../factory/references/evidence.md). Do not route back to this wrapper; continue with the mode below. Use native Codex agents with fresh independent review, inheriting the current model unless the user chooses otherwise.

Write the observed behavior, expected behavior, affected entry point and reproduction conditions. Pin the baseline before edits. Research root cause rather than immediately patching the symptom; keep competing hypotheses distinguishable.

Have an implementer make the smallest adequate repair and a focused regression test. The verifier must establish that the SAME test fails on baseline due to the intended behavior and passes on the repaired candidate. Use the shared repro helper with a narrow expected failure pattern. Import errors, unavailable services, collection errors and arbitrary nonzero exit codes are not reproductions.

Inspect whether the test would fail if the fix were removed, whether mocks conceal the defect and whether related valid behavior regressed. Run tamper detection, applicable regression tests and independent review.

If reproduction cannot be established, report the attempted diagnosis/change and exact missing evidence as blocked. Do not relabel the task, weaken a test or claim a verified fix. PR delivery follows the shared authorization rules.
