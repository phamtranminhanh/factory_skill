# Delivery, CI and connected systems

## Authorized local and PR delivery

A factory invocation does not itself authorize publishing. Read the user's requested deliverable and prior authorization. Local changes and verification can proceed within normal coding scope. If PR creation is authorized, perform it without asking again; if not, prepare the verified diff and draft description first and ask only when publishing is necessary to satisfy the task.

Before delivery, read the current gate and recompute it. Inspect `git status` and changed-file inventory; no unrelated user files may be staged. Commit the exact verified candidate on the task branch when appropriate. The helper's content fingerprint is stable across an identical-content commit, but changes from format hooks invalidate it. A published PR should be based on a clean working tree, with recorded HEAD and no uncommitted verified source left behind.

Use a connected GitHub/GitLab tool when available; otherwise use the configured authenticated forge CLI. Verify the remote host and target base branch from the repo. Do not guess a project/organization or silently install a new service connection. Use a structured request or body file to preserve the exact PR description. Include: problem/result, scope, criterion evidence, actual test commands/outcomes, reproduction status, review findings, skipped checks and known limitations. Never post raw logs containing credentials or unrelated personal paths.

PR creation is not successful delivery until the forge reports the expected PR URL, head commit and base branch. Compare the remote head with the verified local commit. If a hook/rebase/retry moved the source, re-run affected checks and independent review. A PR draft may be opened early only when publishing is already authorized and a real acceptance criterion needs it; label it unverified until gates finish.

Do not automatically merge or deploy. Those are separate user requests and must recheck the current head, evidence, CI and relevant authorization. A PR-specific failure should leave a local verified artifact and concrete blocker, not discard implementation.

## CI

Prefer existing repository workflows and declared build/test commands. On `factory-cifix`, inspect the exact failed run and commit, distinguish environmental failure from source regression, and verify on the corrected commit. Green local tests do not imply remote CI passed. Read-only polling is allowed within an active task; use bounded waits, preserve progress communication, and stop if a required external action cannot be completed. If the user asked to watch to completion, continue in the active chat; do not create a background automation merely to watch one run.

CI retries/reruns that consume resources or alter external state must fit the user's request. Do not disable mandatory jobs, weaken assertions or change branch protection to make CI green. Report unavailable CI as unavailable; use a recorded log artifact for offline diagnosis when live access is missing.

## Issue trackers, context and notifications

GitHub/GitLab issue URLs, Jira, Linear and monday.com can supply ticket context through available connectors or supported CLIs. Discover the actual tool first. If no connection exists, accept pasted/exported ticket content; do not claim automatic sync. Write-back transitions and comments only when explicitly requested. Match the real tracker schema, not guessed transition IDs.

Slack/Teams/email notifications are opt-in actions requiring explicit user authorization; do not send just because a blocker exists. Keep user questions in the current chat otherwise. MCP is a transport available through the host; these skills are not a new MCP server.

## Evidence handoff

Return the PR link or local changed files, verification summary and remaining limitations. Keep the run path so `$factory-resume`/`$factory-pr` can inspect the exact artifacts. The ledger is outside source; don't commit it wholesale. A sanitized verification report may accompany a PR if useful and within scope.
