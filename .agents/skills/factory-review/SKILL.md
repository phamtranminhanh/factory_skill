---
name: factory-review
description: "Independently review an existing diff, branch or pull request through factory evidence checks, with actionable findings and no automatic code changes or external comments."
---

# factory-review

Run the shared Factory workflow with kind `code_review`. Read [the common contract](../factory/SKILL.md), then [workflow](../factory/references/workflow.md), [agent roles](../factory/references/agents.md), and [evidence tooling](../factory/references/evidence.md). Do not route back to this wrapper; continue with the mode below. Use native Codex agents with fresh independent review, inheriting the current model unless the user chooses otherwise.

Establish the review target and baseline: PR head versus its merge base, or the user's intended local diff. Never silently review the wrong checkout or an incidental merge commit. Use an isolated checkout for another branch rather than overwriting dirty user work.

Keep the source unchanged. Read all changed paths and relevant callers; inspect acceptance criteria, tests, configuration, migrations and permissions as applicable. Run existing checks when useful and feasible, recording exactly what ran. Do not repair findings during review.

Delegate a fresh reviewer with the original review request and source artifacts. Distinguish functional bugs from low-severity style preferences. Cite precise existing locations or explicit deleted-file/baseline artifacts. A valid citation does not establish a valid finding; explain the reachable failure.

Audit every diff against the **Factory Clean Code Checklist**:
- [ ] **Function Size & SRP**: Are functions < 30 lines and doing only one thing? Are components < 150 lines?
- [ ] **Guard Clauses**: Are nested if-else blocks avoided using early return?
- [ ] **Naming Quality**: Are booleans prefixed with `is/has/can/should`? Are variables descriptive (no `data`, `res`, `temp`, `cb`)?
- [ ] **Type Integrity**: Is there any usage of `any` or `@ts-ignore`? (Strictly FAIL if present).
- [ ] **Shadcn Style Integrity**: Are shadcn components free from color/border/font overrides in `className`? (FAIL if custom `bg-*` or `text-*` classes override standard shadcn components; must use `variant` or `size` props instead).
- [ ] **Separation of Concerns**: Is business logic/API querying decoupled from UI presentation?
- [ ] **Dead Code**: Are there remaining `console.log` statements, unused imports, or commented code?
- [ ] **Error Handling**: Are catch blocks handling errors explicitly rather than swallowing them?

The report can be successfully completed while the reviewed CODE verdict is FAIL. For the ledger's report-completion review, verify that the REPORT satisfies the user's review request; put its code findings in the report and clearly label the code verdict. Do not turn code findings into a claim that the review task itself was never delivered.

Record the report as a deliverable, obtain an independent review of its accuracy, and preserve the repository fingerprint. Post inline PR comments only if explicitly requested; otherwise return findings in chat.
