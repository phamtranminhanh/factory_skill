---
name: factory
description: Run a Codex software factory with task-specific planning, delegated implementation, independent review, executable verification, bounded repairs, and an evidence-backed handoff. Use for factory requests or when the user asks for an orchestrated agent team; route to the matching factory task skill.
---

# Factory

Act as the coordinator of a Codex team. Reuse the current environment's agent and execution tools; do not launch `no_human`, require Claude, or use `codex exec` to create extra agents when native delegation is available. Model selection inherits the current session unless the user chooses otherwise.

## Route by deliverable

| Request | Read sibling skill | Internal kind |
|---|---|---|
| New behavior | `../factory-feature/SKILL.md` | feature |
| Defect/regression | `../factory-fixbug/SKILL.md` | bugfix |
| Broken CI/build | `../factory-cifix/SKILL.md` | ci_fix |
| Missing test coverage | `../factory-testgap/SKILL.md` | test_gap |
| Requirement-to-test mapping | `../factory-traceability/SKILL.md` | traceability |
| Root-cause investigation/audit | `../factory-investigate/SKILL.md` | investigation |
| Review a branch/PR | `../factory-review/SKILL.md` | code_review |
| Architecture/design proposal | `../factory-design/SKILL.md` | design_doc |
| Behavior-preserving restructuring | `../factory-refactor/SKILL.md` | refactor |
| Documentation changes | `../factory-docs/SKILL.md` | docs |
| Continue a recorded run | `../factory-resume/SKILL.md` | preserve original kind |
| Deliver an already-verified change | `../factory-pr/SKILL.md` | preserve original kind |

Explicit user choice wins. If the deliverable conflicts with the selected type, explain the mismatch and resolve the actual desired outcome before spending implementation rounds. Investigations and designs produce reports; they do not silently become implementation.

Read [workflow.md](references/workflow.md) and [agents.md](references/agents.md) for every run. Read [evidence.md](references/evidence.md) before running gates. Read [delivery.md](references/delivery.md) only for PR/CI/external integrations, and [capabilities.md](references/capabilities.md) when discussing coverage relative to no_human. These are a shared installed suite: if a sibling/reference is missing, report an incomplete installation rather than silently invent its contract.

## Non-negotiable evidence rules

- A coder's self-check is advisory. Use an independent reviewer with a fresh conversation and original task/artifacts, not the coder's transcript. Same model is allowed; same author session is not independent.
- Mechanical checks are real commands and receipts, never claims in an agent message. Bind review and verification to the same candidate fingerprint. Revalidate after candidate changes.
- An unavailable required check is `NOT RUN`/`BLOCKED`, never PASS. Bugfixes require behavioral failure on the baseline and success after the fix, or an explicit disclosure that the verified workflow could not complete.
- Detect weakening tests before accepting their green output. Flagged changes require an independent, criterion-specific explanation; coder self-justification is insufficient.
- Never quietly turn off guards, reduce acceptance criteria, reclassify bugfix as feature, or enlarge retry bounds to get a green gate.
- Track a real blocker and resumable state when unable to proceed. Do not imply persistent background workers or future monitoring from a skill invocation.

## Local support

A local dashboard is included. Read [dashboard.md](references/dashboard.md) when the user asks to open, start or customize it. New runs register automatically; the dashboard reads their real state and evidence. It does not start background agents.

`python3 scripts/factory_run.py --help` exposes a standard-library-only evidence ledger. Resolve this path relative to this skill, not the target repo. It stores runs beneath the repository's Git common directory (`factory-runs/`), outside the candidate source tree. Only the coordinator writes the ledger; delegated writers receive the workspace and their task, not authority to edit evidence records.

The helper verifies local facts and declared review records. It does not enforce OS isolation, authenticate reviewer identities, measure unexposed model costs, or replace remote CI. Preserve these limitations in user-facing claims.
