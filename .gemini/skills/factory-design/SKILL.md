---
name: factory-design
description: "Create a software architecture or implementation design through independent factory proposals and review, producing a decision-ready document without silently implementing it."
---

# factory-design

Run the shared Factory workflow with kind `design_doc`. Read [the common contract](../factory/SKILL.md), then [workflow](../factory/references/workflow.md), [agent roles](../factory/references/agents.md), and [evidence tooling](../factory/references/evidence.md). Do not route back to this wrapper; continue with the mode below. Use native Codex agents with fresh independent review, inheriting the current model unless the user chooses otherwise.

Produce a design report with problem, constraints, explored options, chosen approach, interfaces/data changes, compatibility/migration, risks and an executable validation plan. Ground proposals in the existing codebase; do not invent services or permissions.

For consequential alternatives, use independent minimal-change, risk-first and test-first proposals and synthesize a reasoned decision. Small designs need only a concise plan and independent review. Clearly label assumptions requiring a product decision.

Do not edit product source or implement the design. Store the report in the run directory and use the deliverable hash in review JSON. The reviewer checks consistency, criterion coverage, feasibility and unhandled failure paths.

Deliver the document contents and unresolved decisions. If the user requests committing documentation into the repository as the deliverable, route through factory-docs after clarifying that this is a documentation change; do not violate the report-only run's unchanged-tree gate.
