# Executable Tasks (Sub-Issues): [{id}] {title}

| Field | Value |
|---|---|
| **Feature ID** | {id} |
| **Total Sub-Tasks** | {total_tasks} |
| **Execution Order** | Sequential (Task 1 -> Task 2 -> Task 3) |
| **Ready for Development** | [ ] Yes (Checked and approved by Dev Lead) |

---

### [Sub-Task 01]: {task_01_title}
- **Kind**: `feature`
- **Target Files to Create / Modify**:
  - `src/contracts/{feature_slug}.ts` (API Schema)
  - `src/lib/services/{feature_slug}.ts` (Service logic)
  - `tests/unit/{feature_slug}.test.ts` (Unit test)
- **Reusable Assets**:
  - Uses `@/lib/db.ts`
- **Step-by-Step Instructions**:
  1. Define the Zod schema for request validation.
  2. Implement the business logic function handling happy path and unhappy cases.
  3. Write unit tests covering valid input, boundary conditions, and invalid inputs.
- **Verification Commands (Must run in terminal and pass with exit 0)**:
  ```bash
  npm run test tests/unit/{feature_slug}.test.ts
  npm run type-check
  ```
- **Acceptance Criteria**:
  - [ ] Schema validates correct input.
  - [ ] Throws descriptive error for invalid input.
- **Definition of Done**:
  - [ ] All tests pass without regression.
  - [ ] Code follows existing project conventions.

---

### [Sub-Task 02]: {task_02_title}
- **Kind**: `feature`
- **Target Files to Create / Modify**:
  - `src/app/api/{feature_slug}/route.ts` (API Endpoint)
  - `tests/integration/{feature_slug}_api.test.ts`
- **Step-by-Step Instructions**:
  1. Create Route Handler handling POST / GET requests.
  2. Parse body using schema from Sub-Task 01.
  3. Wire up service call and return standard JSON response.
- **Verification Commands**:
  ```bash
  npm run test tests/integration/{feature_slug}_api.test.ts
  ```
- **Definition of Done**:
  - [ ] API returns 200 on success, 400 on validation failure, 401 if unauthenticated.

---

### [Sub-Task 03]: {task_03_title}
- **Kind**: `feature`
- **Target Files to Create / Modify**:
  - `src/app/(main)/{feature_slug}/page.tsx`
  - `src/components/features/{feature_slug}/...`
- **Reusable Assets**:
  - Reuses `@/components/ui/button.tsx`, `@/components/ui/input.tsx`
  - Reuses layout from `src/app/(previews)/feature-{id}/page.tsx`
- **Step-by-Step Instructions**:
  1. Move or wire up the UI component created in preview mode to the real API endpoint.
  2. Handle loading, error, and empty states.
  3. Verify responsive layout on mobile and desktop viewports.
- **Verification Commands**:
  ```bash
  npm run build
  npm run test
  ```
- **Definition of Done**:
  - [ ] Full end-to-end user flow operates smoothly without console errors.
  - [ ] Passes independent review via `factory-review`.
