---
name: factory-traceability
description: "Map requirements or acceptance criteria to automated tests, code entry points and execution evidence, and fill authorized gaps using the factory workflow."
---

# factory-traceability

Run the shared Factory workflow with kind `traceability`. Read [the common contract](../factory/SKILL.md), then [workflow](../factory/references/workflow.md), [agent roles](../factory/references/agents.md), and [evidence tooling](../factory/references/evidence.md). Do not route back to this wrapper; continue with the mode below. Use native Codex agents with fresh independent review, inheriting the current model unless the user chooses otherwise.

Assign stable criterion IDs and build a requirement → production entry point → test → execution receipt map. Distinguish a named test that exists from a test that actually ran and a test that actually asserts the requirement.

Resolve contradictory requirements before authoring tests. Add or link tests only within the requested scope. Mark uncovered, ambiguous, stale and manual-only criteria explicitly. If asked only for a read-only mapping report, use a report-only investigation run instead of forcing source changes.

The independent reviewer checks semantic linkage: a similar test name is not proof. Execute relevant tests for any changed coverage. Preserve references to the exact candidate and command outputs.

Deliver the traceability table and any authorized test changes; do not mark all requirements satisfied by copying titles into a matrix.
