---
name: factory-investigate
description: "Investigate a software problem or audit behavior with a factory research team, cited evidence, hypothesis checks and an independently reviewed report; do not implement a fix implicitly."
---

# factory-investigate

Run the shared Factory workflow with kind `investigation`. Read [the common contract](../factory/SKILL.md), then [workflow](../factory/references/workflow.md), [agent roles](../factory/references/agents.md), and [evidence tooling](../factory/references/evidence.md). Do not route back to this wrapper; continue with the mode below. Use native Codex agents with fresh independent review, inheriting the current model unless the user chooses otherwise.

Keep the target repository unchanged. Write the report in the run directory, not into product source. Separate observations, hypotheses, experiments and conclusions. Scope each researcher to a concrete question and source area.

Prefer reproductions, logs and production call paths over confident explanations. State confidence in words tied to evidence, and preserve competing explanations when evidence does not distinguish them. Do not interpret a diagnostic request as authorization to repair, publish, alter accounts or deploy.

A fresh reviewer checks whether each conclusion follows from its cited evidence and whether mandatory questions are answered. Record the report with `deliverable`, include its hash in review JSON, and gate it against the unchanged source fingerprint.

Deliver the actual report, root cause if established, unresolved questions and a concrete next action. A proposed fix is a proposal, not an implemented change.
