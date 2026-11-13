---
name: app-feature-issues
description: Turn an app idea (typed text like "make an app like WhatsApp") or a document (proposal, spec, PRD, RFP file) into small features, one GitHub issue per feature. Use whenever the user asks to make/build/clone an app like X, gives a proposal/spec file to split into tickets, or says "split this into features/issues". Output is the list of issues on GitHub, created only after the user confirms the list.
---

# App Idea → One Issue per Feature

**Input:** either
- **text**, e.g. "make an app like WhatsApp" (optionally with constraints: platform, MVP vs full, tech stack, target users), or
- **a file**, e.g. a proposal/spec/PRD/RFP (`.md`, `.txt`, `.docx`, `.pdf`, `.xlsx`). Read all of it (use the docx/pdf/xlsx skills as needed); every requirement must land in exactly one issue, or in out-of-scope/open questions. Quote the source location in each issue.

**Output:** the list of issues on **GitHub**, one issue per feature, in the target repo (ask for `owner/repo` if not given, or use the current repo's remote). Local drafts are written first to `issues/<app-name>/` (one `NNN-feature-name.md` per feature plus `INDEX.md`) so the user can review them; nothing reaches GitHub until step 6.

Do not start coding the app. **Never push or create issues on GitHub without the user's explicit confirmation of the final list (see step 6).** The goal is a reviewable feature breakdown.

## Workflow

### 1. Frame the app
- Identify the reference app and the user's constraints. If something big is unclear (platform: mobile/web/both; MVP or full parity; scale), make a sensible default, state it at the top of `INDEX.md` under **Assumptions**, and proceed. Ask only if the answer would change the whole breakdown.
- Define what is **in scope** and **out of scope** (e.g. for a WhatsApp-like MVP: no payments, no business API, no status/stories).

### 2. Decompose into features
- List the major **areas** (epics), then the **features** in each. For a WhatsApp-like app, areas include: Accounts & Onboarding, Contacts, 1:1 Messaging, Group Chat, Media Sharing, Voice/Video Calls, Notifications, Presence & Receipts, Search, Settings & Privacy, Security/E2EE, Backup, Platform/Infra.
- **One feature = one issue.** A feature is a single user-visible capability that one dev can build and QA can verify (about 1–5 days). If bigger, split into two features; if trivial, merge into a neighbor.
- Include foundation issues (project setup, auth backend, realtime messaging infra, CI/CD, design system) as their own features.
- Every feature must be non-overlapping with the others.

### 3. Write each issue
Use `references/issue-template.md`. Each issue must be **detailed enough for a dev to start without asking questions**: title (verb-first), area, priority (P0 MVP-critical → P3 nice-to-have), size (S/M/L), dependencies, suggested role, plus overview, user story, functional requirements (specific rules, limits, states), user flow, testable acceptance criteria, edge cases & error handling, non-functional requirements, technical notes (marked Suggestion), testing notes, out of scope and definition of done. Never leave a section as a one-liner placeholder.

### 4. Write `INDEX.md`
- App summary, assumptions, in/out of scope.
- Table grouped by area: ID, feature, priority, size, role, depends on.
- Suggested build order (phases: Foundation → Core MVP → Enhancements), driven by dependencies.
- Counts: total issues, per area, per priority.

### 5. Verify and report
- Check dependency IDs exist with no cycles, numbering is contiguous, every issue has acceptance criteria, no duplicate features.
- Tell the user the output path, issue counts per area, and the build order. Offer to adjust granularity/scope, push the issues to GitHub (step 6), or export CSV.

### 6. Confirm, then push to GitHub (only if the user wants it)
Pushing is outward-facing and hard to undo, so it is always gated. Confirm **in plain chat text**, not a pop-up dialog (dialogs can hide the list).
1. **Print the full list in chat**: every issue grouped by area with ID, title, priority, size, role, depends-on. Never truncate or summarise. Also give the review files: `issues/<app-name>/INDEX.md` and each `NNN-*.md`.
2. State the target repo (`owner/repo`) and the active `gh` account (`gh auth status`). If that account cannot see the repo, ask the user to switch (`gh auth switch --user <name>`); never switch accounts or read tokens silently.
3. **Ask the user to reply** with one of: `push all`, `push P0 only` (or another subset), an edit (remove, rename, merge, split, re-prioritise), or `cancel`. Then stop and wait.
4. After any edit, update the files and `INDEX.md`, re-print the full list, and ask again. Earlier approval does not carry over to a changed list.
5. Only after an explicit push reply: create labels if missing, then issues in ID order with `gh issue create --repo owner/repo --title "[NNN] ..." --body-file <file> --label <area>,<priority>`. Afterwards replace dependency IDs (`NNN`) with real issue numbers (`#123`) via `gh issue edit`.
6. On cancel, report that nothing was pushed. After a push, report the issue URLs and any failures.

## Quality rules
- Features describe behavior, not implementation; mark tech suggestions as "Suggestion".
- Acceptance criteria must be testable, not vague.
- Be specific and concrete (numbers, limits, states, error messages) rather than generic; don't pad with filler.
- Write output to the user's working directory, never inside the skill folder.
