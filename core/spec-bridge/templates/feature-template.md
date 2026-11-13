# [{id}] {title}

| Field | Value |
|---|---|
| **Area (Epic)** | {area} |
| **Priority** | P0 (MVP-critical) / P1 (Important) / P2 (Nice-to-have) / P3 |
| **Size** | S (1-2 days) / M (3-4 days) / L (5 days) |
| **Suggested Role** | Backend / Frontend / Fullstack / QA |
| **Depends on** | {depends_on} (or "none") |

---

## 1. Overview
{overview} (2-3 sentences explaining what this feature is and the business value).

## 2. User Stories
**Primary User Persona:** {persona}

**Primary Story (Happy Path):**
> As a {persona}, I want to {action}, so that {benefit}.

**Additional Stories:**
- As a {secondary_persona}, I want to {action}, so that {benefit}.

## 3. Functional Requirements
1. The system must allow users to ...
2. Input validation rules: ...
3. State transitions and limits: ...

## 4. User Flow
1. User navigates to ...
2. User performs action ...
3. System responds with ...

## 5. Happy Case & Unhappy Cases

### Happy Case
End-to-end successful interaction description.

### Unhappy Cases Table
| Situation / Failure | Expected System Behavior & User Feedback |
|---|---|
| Invalid input / Validation error | Highlight invalid field with error message |
| Unauthorized / Session expired | Redirect to login with return URL preserved |
| Network offline / Timeout | Show retry banner, preserve user draft data |
| Resource limit exceeded | Inform user with friendly message and upgrade prompt |

## 6. Acceptance Criteria (BDD / Gherkin Format)
- [ ] **Scenario 1**: Given {initial state}, when {action occurs}, then {expected outcome}.
- [ ] **Scenario 2**: Given {error state}, when {action occurs}, then {expected failure message}.

## 7. Edge Cases & Non-Functional Requirements
- **Security**: Authentication checks, rate limiting, data privacy.
- **Performance**: Response within 200ms, responsive on mobile screens.

## 8. Definition of Done (DoD)
- [ ] Code implemented and passes unit & integration tests.
- [ ] UI matches design system tokens and component library.
- [ ] Acceptance criteria verified by QA.
- [ ] Independent code review passed with no critical issues.
