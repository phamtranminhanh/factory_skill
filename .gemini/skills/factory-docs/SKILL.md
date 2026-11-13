---
name: factory-docs
description: "Change repository documentation through a scoped factory workflow with factual/source validation and independent review; preserve runtime behavior."
---

# factory-docs

Run the shared Factory workflow with kind `docs`. Read [the common contract](../factory/SKILL.md), then [workflow](../factory/references/workflow.md), [agent roles](../factory/references/agents.md), and [evidence tooling](../factory/references/evidence.md). Do not route back to this wrapper; continue with the mode below. Use native Codex agents with fresh independent review, inheriting the current model unless the user chooses otherwise.

Identify the audience, requested facts and documentation destination. Verify examples, paths, configuration defaults and public APIs against current source or authoritative documentation. Avoid copying historical comments as current guarantees.

Keep runtime behavior unchanged. For prose-only changes, required executable checks may be empty if no relevant docs check exists; record that choice at intake. Run existing doc builds, link checks or snippet checks when available. Do not run costly unrelated suites just to produce a green log.

Use a short plan and coordinator implementation for small changes, but retain independent factual review. The tamper detector is still run to verify the diff did not quietly alter test files. Agent instructions and gate configuration deserve full review even if they are Markdown.

Deliver the edited docs and summarize factual validation; don't claim application behavior was tested when only docs were checked.
