# [NNN] <Verb-first feature title>

| Field | Value |
|---|---|
| Area | <epic, e.g. 1:1 Messaging> |
| Priority | P0 / P1 / P2 / P3 |
| Size | S / M / L |
| Suggested role | Backend / Frontend / Mobile / QA / DevOps / Design |
| Depends on | NNN, NNN (or "none") |

## Overview
2–4 sentences: what the feature is, why it matters, and where it sits in the product.

## User stories
**Who:** <specific persona and context, e.g. "A first-time user who owns a smartphone and no account yet">

**Primary story (happy case)**
> As a <specific user in a specific situation>, I want <concrete capability>, so that <measurable benefit>.

**Additional stories** (1–3, other roles or situations: returning user, admin, recipient, user who denied a permission)
- As a <user>, I want <...>, so that <...>.

## Functional requirements
- Numbered, specific behaviours the feature must have (inputs, rules, limits, states).

## User flow
1. Step-by-step happy path from the user's point of view.

## Happy case
One sentence describing what success looks like end to end (steps are in User flow).

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| <what goes wrong: invalid input, offline, permission denied, limit reached, failure> | <exactly what the user sees / the system does> |

## Acceptance criteria
- [ ] Given <context>, when <action>, then <result>
- [ ] ...

## Edge cases & error handling
- Offline, permission denied, invalid input, limits, concurrency, failures and what the user sees.

## Non-functional requirements
- Performance, security/privacy, accessibility, platform notes.

## Technical notes (Suggestion)
- Optional hints: APIs, data model, libraries. Mark as suggestions, not requirements.

## Testing notes
- Key scenarios QA should cover.

## Out of scope
- What this issue does NOT include.

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
