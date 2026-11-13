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

## User story
As a developer, I want a configured monorepo with CI/CD so that features ship safely.

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
