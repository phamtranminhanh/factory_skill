# Scope relative to no_human

Reference implementation inspected: `no-human-ai/no_human`, commit `cdcbd0af086890eb4ecdbece1c1ca8dc168e5907` (package version 0.2.4). The suite adapts the workflow to native Codex sessions. It is not a port of the daemon, desktop application or complete backend. Do not claim feature parity without the distinctions below.

| Capability | This skill suite |
|---|---|
| Eight repo task kinds | Separate entry skills: feature, fixbug, cifix, traceability, testgap, investigate, review, design |
| Additional task routes | refactor, docs, resume and PR handoff |
| Context discovery and acceptance criteria | Coordinator workflow, project-scoped |
| Plan before code | Recorded plan; optional proportional multi-proposal planning |
| Human plan approval | Honored when user requests it; no new mandatory approval |
| Coder/researcher/supervisor/reviewer roles | Native subagents plus coordinator supervision at handoffs |
| Automatic per-tool supervisor hooks | Not implemented; host-dependent, never claimed |
| Fresh-context adversarial review | Required distinct session; same model allowed |
| Checklist verdict and citation validation | Structured review artifact and mechanical verdict checks; source citation existence is checked |
| Test-tamper detection | Vendored upstream detector plus Unicode-safe Git snapshot wrapper; heuristic limits disclosed |
| Tamper adjudication | Independent criterion-specific review of every flagged reason |
| Red-before / green-after reproduction | Actual temporary baseline worktree and command receipts; required for bugfix completion |
| Local tests/build/lint/type/UI checks | Explicit project commands; no invented success for missing commands |
| Wiring/type/lint evidence | Use project tooling and independent source inspection; upstream specialized analyzers not ported |
| Project-specific verifiers | Explicit rules in review contract; mandatory unknowns block (stricter than upstream advisory unavailability) |
| Bounded repairs and blockers | Recorded rounds, wall-time and blocker/resume commands; coordinator controls agent lifetime |
| Token/cost accounting | Use host data if exposed, otherwise unknown; no custom billing ledger |
| Worktree and candidate identity | Git worktree procedure plus content fingerprint; no additional OS sandbox |
| Concurrent task workers | Host agent slots during active invocation only; no daemon pool |
| Multi-repo work | Separate evidence run per repo and parent manifest; all required repos must succeed |
| PR/MR delivery and remote CI | Available forge tools/CLI plus head verification; no built-in credentials |
| Tracker intake and write-back | Connected tools/pasted input; write-back only when authorized; no poller |
| Slack/Teams notifications | Existing connectors if explicitly authorized; no automatic messaging |
| Persistent memory/learning | Project-scoped lesson proposal, authorized storage; no autonomous harvesting service |
| Pause/resume and checkpoints | Durable local ledger, continued through a user-invoked session |
| Watcher/recovery after chat ends | Not supplied; no claim to continue when the session ends |
| Task board and evidence dashboard | Local read-only web dashboard, live ledger projection, filters, reports and clearly separated demo; no desktop app or worker controls |
| Standalone MCP server/GitHub Action | Not supplied; existing host/service tools can be used |
| Self-evaluation/benchmark harness | Offline regression tests for the helper and a bounded forward-test of the skill; not upstream benchmark parity |

## Evidence limits

Local evidence files can be edited by a process with user filesystem access. Review independence is established by actual delegation and preserved artifacts, not by a trusted attestation service. Fingerprints omit ignored state and remote services. The copied tamper detector is best-effort for its recognized test syntax. None of this proves all bugs are caught.

Full backend/provider neutrality is not required here: native Codex handles model execution and account access. The suite never reads or copies auth caches. Any future API/CLI integration must be designed and authorized separately rather than hidden inside a skill.
