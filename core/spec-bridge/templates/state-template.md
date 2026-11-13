# Factory State Board: {app_name}

Last Updated: {timestamp}

## Global Project Milestones
- [ ] Phase 0: Project Setup & Foundation (CI/CD, Design System, Base Shell)
- [ ] Phase 1: Core MVP Features (P0)
- [ ] Phase 2: Essential Enhancements (P1)
- [ ] Phase 3: Secondary Features (P2/P3)

---

## Active Pipeline Status

| Feature ID | Feature Name | Priority | Status | Assigned Role | Dependencies |
|---|---|---|---|---|---|
| 001 | Project Setup & CI/CD | P0 | DONE | DevOps / Developer | none |
| 002 | ... | P0 | READY_FOR_SPEC | Tech Lead | 001 |
| 003 | ... | P0 | QUEUED | - | 001, 002 |

> **Status Glossary:**
> - `DRAFT`: BA is drafting / clarifying feature.
> - `READY_FOR_SPEC`: Feature approved by BA, ready for Tech Lead & Spec-Kit.
> - `IN_DESIGN`: Designer is prototyping component in preview route.
> - `READY_TO_CODE`: Spec & sub-tasks approved by Dev Lead, ready for Developer Agent.
> - `IN_DEVELOPMENT`: Developer Agent is executing sub-tasks (`factory-feature`).
> - `IN_REVIEW`: `factory-review` or QA is evaluating PR.
> - `DONE`: Merged into main.
