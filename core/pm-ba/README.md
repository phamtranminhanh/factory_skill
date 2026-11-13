# factory_skill

A Claude Code skill for Business Analysts and product teams: turn an **app idea or a document** into a reviewed backlog of **GitHub issues, one issue per feature**.

## What it does

| | |
|---|---|
| **Input** | Text such as `make an app like WhatsApp`, **or** a file (proposal, spec, PRD, RFP: `.md`, `.txt`, `.docx`, `.pdf`, `.xlsx`) |
| **Output** | One GitHub issue per feature in a repo you choose, with labels and linked dependencies |

The skill is `app-feature-issues` (`.claude/skills/app-feature-issues/`).

## How it works

1. **Frame**: identifies the reference app or document, states assumptions, and sets in-scope and out-of-scope.
2. **Decompose**: groups work into areas (epics) and features. One feature is one issue, sized for one dev for about 1–5 days. Foundation work (setup, CI/CD, realtime infra) gets its own issues.
3. **Write drafts**: creates `issues/<app-name>/` with one `NNN-feature.md` per feature plus an `INDEX.md` table and build order.
4. **Verify**: checks numbering, dependencies (no cycles) and that every issue has acceptance criteria.
5. **Confirm**: prints the **full list in chat** and waits for your reply. Nothing is pushed until you say so.
6. **Push**: creates labels and issues in ID order via `gh`, then replaces dependency IDs with real `#` issue numbers.

## What each issue contains

Overview, user story, functional requirements, user flow, acceptance criteria, edge cases and error handling, non-functional requirements, technical notes (marked as suggestions), testing notes, out of scope and definition of done. Plus area and priority labels (P0 MVP to P3 nice-to-have), size (S/M/L), suggested dev role and dependencies.

## Usage

Start Claude Code in this folder and type, for example:

```
make an app like WhatsApp
```
```
split proposal.pdf into issues and push to owner/repo
```

At the confirmation step reply with one of:

- `push all`: create every issue
- `push P0 only`: create only the MVP issues (or name another subset)
- an edit such as `remove 009` or `merge 012 and 013`: drafts are updated and the list is shown again
- `cancel`: nothing is pushed

## Requirements

- [Claude Code](https://claude.com/claude-code)
- [GitHub CLI](https://cli.github.com/) (`gh`) logged in to an account with access to the target repo. Check with `gh auth status`; switch with `gh auth switch --user <name>`.

## Safety

- The skill never creates or edits GitHub issues without your explicit confirmation of the current list. Any change to the list requires a new confirmation.
- It never switches `gh` accounts silently.
- It does not write or run application code; it only produces the feature breakdown.

## Repository layout

```
.claude/skills/app-feature-issues/
  SKILL.md                     # skill instructions
  references/issue-template.md # issue body template
issues/<app-name>/             # generated drafts (example: whatsapp-clone)
```

## Example

`issues/whatsapp-clone/` holds a 31-issue backlog (12 P0, 9 P1, 8 P2, 2 P3) across Foundation, Accounts, Contacts, 1:1 Messaging, Group Chat, Media, Calls, Notifications, Search, Privacy, Security and Backup.
