# User Guide: app-feature-issues

Turn an app idea or a requirements document into a reviewed set of GitHub issues, one issue per feature. This guide is for Business Analysts, product owners and anyone who assigns work to developers.

---

## 1. Before you start

You need:

| Requirement | How to check |
|---|---|
| [Claude Code](https://claude.com/claude-code) installed | `claude --version` |
| [GitHub CLI](https://cli.github.com/) installed and logged in | `gh auth status` |
| Access to the target GitHub repo | `gh repo view owner/repo` |
| This repo cloned locally | `git clone https://github.com/phamtranminhanh/factory_skill.git` |

Using more than one GitHub account? Make sure the **active** one can see the target repo. Switch with:

```
gh auth switch --user <account-name>
```

Open your terminal **in the repo folder** and start Claude Code there. The skill lives in `.claude/skills/app-feature-issues/` and only loads from this folder.

---

## 2. Quick start (5 steps)

1. **Ask.** Type what you want:
   ```
   make an app like WhatsApp
   ```
2. **Wait for drafts.** The skill writes one file per feature into `issues/<app-name>/`.
3. **Review.** It prints the full list in chat. Open `issues/<app-name>/INDEX.md` for the table, or any `NNN-*.md` for a full issue.
4. **Reply.** Say `push all`, `push P0 only`, an edit, or `cancel`.
5. **Done.** Issues appear in your GitHub repo with labels and linked dependencies.

---

## 3. Giving input

### Option A: Text

Describe the app or feature set. More detail gives a better breakdown.

```
make an app like WhatsApp
```
```
make an app like Uber for mobile only, MVP, push to owner/repo
```
```
make a booking app like Airbnb with host and guest roles
```

Useful details to include: platform (mobile/web), MVP or full, target users, tech stack, the GitHub repo to push to.

### Option B: A file

Give a proposal, spec, PRD or RFP (`.md`, `.txt`, `.docx`, `.pdf`, `.xlsx`):

```
split docs/proposal.pdf into issues
```

The skill reads the whole file. Every requirement ends up in exactly one issue, or in out-of-scope / open questions, and each issue quotes where in the file it came from.

If you don't say which repo to use, the skill asks.

---

## 4. What you get

### Local drafts (for review)

```
issues/<app-name>/
  INDEX.md              # summary, assumptions, table of all features, build order, counts
  001-set-up-project.md # one file per feature
  002-...
```

`INDEX.md` has the in-scope and out-of-scope lists, a table grouped by area (ID, feature, priority, size, role, dependencies) and a suggested build order.

### Each issue contains

| Section | Purpose |
|---|---|
| Header table | Area, priority (P0–P3), size (S/M/L), suggested dev role, dependencies |
| Overview | What and why |
| User stories | Who, a primary story (the happy case) and additional stories |
| Functional requirements | Specific rules, limits and states |
| User flow | Step-by-step path |
| Happy case | What success looks like |
| Unhappy cases | Table of situation and expected behaviour |
| Acceptance criteria | Checkboxes QA can test |
| Edge cases & error handling | Failures and special situations |
| Non-functional requirements | Performance, security, accessibility |
| Technical notes | Suggestions only, not requirements |
| Testing notes | What QA should cover |
| Out of scope | What this issue does not include |
| Definition of done | Completion checklist |

### On GitHub

- One issue per feature, titled `[NNN] Verb-first title`.
- Two labels each: an **area** (for example "Group Chat") and a **priority** (P0–P3).
- Dependencies written as real links, for example `Depends on #16`.

### Priorities

| Label | Meaning |
|---|---|
| P0 | MVP-critical; the product doesn't work without it |
| P1 | Important, follows the MVP |
| P2 | Enhancement |
| P3 | Nice to have |

### Sizes

S, M and L are rough hints for planning, not estimates. One issue is meant to be about 1–5 days for one developer.

---

## 4a. Reviewing before you push

Nothing is created on GitHub until you say so. Before replying, you can:

- Read the full list the skill prints in chat.
- Open `issues/<app-name>/INDEX.md` for the table.
- Open any `issues/<app-name>/NNN-*.md` for one issue in full.
- Ask in chat: `show 017`, or `show all P0 issues`.

## 5. Confirming and pushing

The skill stops after printing the list and the target repo (plus the active `gh` account). Reply with one of:

| Reply | Result |
|---|---|
| `push all` | Creates every issue |
| `push P0 only` | Creates only the MVP issues (or name another subset, e.g. `push 001-010`) |
| An edit | The skill updates the drafts and shows the full list again; you must confirm again |
| `cancel` | Nothing is pushed |

### Editing the list

Examples of edits you can ask for:

```
remove 009 and 031
rename 011 to "Show conversation list"
merge 012 and 013
split 018 into photos and videos
change 027 to P1
make the app web-only
```

An earlier approval never carries over to a changed list. After every edit you confirm again.

### What happens on push

1. Missing labels are created.
2. Issues are created in ID order (001, 002, ...).
3. Dependency IDs in each issue are replaced with real GitHub issue numbers.
4. You get the repo link and any failures.

---

## 6. Changing issues after they are on GitHub

Ask for the change, for example:

```
make the user stories more specific
add an unhappy case for phone number already registered to issue 004
```

The skill updates the drafts, shows what will change, and waits for your confirmation before editing the GitHub issues. Editing replaces the old text; it cannot be undone from the skill.

---

## 7. Tips for good results

- **Be specific up front.** Platform, MVP vs full scope and target users change the whole breakdown.
- **Name the repo** in your first message to skip a question.
- **Start with `push P0 only`** to create the MVP first, then push the rest later.
- **Use a file for real projects.** A proposal gives traceable requirements; a one-line idea gives a typical feature set.
- **Review the open questions.** Where the source is vague, the skill makes a sensible assumption and flags it.
- **Assign work from INDEX.md.** The suggested role and dependencies show who can start what, and in which order.

---

## 8. Troubleshooting

| Problem | Fix |
|---|---|
| Skill does not trigger | Start Claude Code from the repo folder; use wording such as "make an app like X" or "split this into issues" |
| `Repository not found` | The active `gh` account can't see the repo. Run `gh auth status`, then `gh auth switch --user <name>` |
| Wrong account pushed to | Run `gh auth status` before confirming; the skill states the account in step 5 |
| Some issues failed to create | The skill reports which ones; ask it to retry only those |
| Dependency still shows `NNN` instead of `#12` | Ask: "link the dependencies on GitHub" |
| `Operation not permitted` on macOS | Grant your terminal access to the folder in System Settings > Privacy & Security > Files and Folders (or Full Disk Access) |
| Too many or too few issues | Ask to merge or split features; one issue should be 1–5 days of work |
| Duplicated issues on GitHub | Don't run `push all` twice; ask the skill to push only missing items |

---

## 9. Safety rules built into the skill

- It never creates or edits GitHub issues without your explicit confirmation of the current list.
- It never switches your `gh` account on its own.
- It does not write or run application code.
- It keeps secrets and private data out of issues.

---

## 10. Example session

```
You:    make an app like WhatsApp, push to phamtranminhanh/factory_skill
Claude: Drafted 31 features in issues/whatsapp/. [prints the full list]
        Target: phamtranminhanh/factory_skill, account: phamtranminhanh.
        Reply: push all / push P0 only / an edit / cancel
You:    remove 009, then push P0 only
Claude: Updated the list (30 features). [prints the list again]
        Confirm: push P0 only (12 issues)?
You:    push P0 only
Claude: Created 12 issues: #1 ... #12.
```
