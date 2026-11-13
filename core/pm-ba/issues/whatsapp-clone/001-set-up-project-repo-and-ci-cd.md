# [001] Set up project, repo and CI/CD

| Field | Value |
|---|---|
| Area | Foundation |
| Priority | P0 |
| Size | M |
| Suggested role | DevOps |
| Depends on | none |

## Overview
Create the shared engineering foundation: a monorepo containing the mobile app, backend services and shared packages, with automated build, test and deploy. Every other issue builds on this, so it must be finished first.

## User stories
**Who:** Developers and QA on the team

**Primary story (happy case)**
> As a developer joining the project, I want to clone the repo and get the mobile app and backend running locally with one documented command, so that I can start contributing on day one without asking for help.

**Additional stories**
- As a reviewer, I want CI to run lint and tests on every pull request and block merging on failure, so that broken code never reaches `main`.
- As a product owner, I want every merge to `main` deployed automatically to staging, so that I can try the latest build the same day.

## Functional requirements
- Monorepo with `mobile/`, `backend/`, `packages/shared` and `infra/` folders and a root README with setup steps
- Branch strategy: `main` protected, feature branches, PRs require 1 review and passing CI
- CI pipeline: install, lint, type-check, unit tests on every PR; build artifacts on merge
- Environments: local (docker-compose), staging and production with separate config and secrets
- Staging auto-deploy on merge to `main`; production deploy by manual approval
- Secrets stored in the CI secret store, never in the repo
- Error tracking and basic logging wired from day one

## User flow
1. Developer clones the repo and runs one setup command
2. Local backend and mobile app start
3. Developer opens a PR; CI runs and reports status
4. After merge, staging is updated automatically

## Happy case
A new developer runs the setup command, the app and backend start locally, a PR passes CI, and the merged change appears on staging automatically.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| A PR has a failing test or lint error | CI fails and merge is blocked until fixed |
| A deploy to staging fails | The previous good version keeps running and the team is alerted |
| A secret is committed by mistake | Secret scanning blocks or flags it before merge |

## Acceptance criteria
- [ ] Mobile app, backend and shared packages build from a clean checkout
- [ ] CI runs lint + tests on every PR
- [ ] Staging deploy runs automatically on merge to main

## Edge cases & error handling
- CI must fail on lint or test errors and block merge
- Builds must be reproducible from a clean checkout (pinned dependency versions)
- A failed deploy must roll back to the last good version

## Non-functional requirements
- CI feedback in under 10 minutes
- No secrets in git history; secret scanning enabled

## Technical notes (Suggestion)
- React Native (or Flutter) for mobile, Node.js/TypeScript or Go for backend, PostgreSQL, Redis, Docker, GitHub Actions.

## Testing notes
- Clone on a fresh machine and follow the README; open a PR with a failing test and confirm it blocks merge.

## Out of scope
- Feature code, production monitoring dashboards.

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
