# Technical Plan: [{id}] {title}

| Field | Value |
|---|---|
| **Feature ID** | {id} |
| **Architect / Dev Lead** | Tech Lead Agent |
| **Architecture Pattern** | Next.js App Router / Server Actions / REST API |
| **Status** | DRAFT / REVIEWED / APPROVED |

---

## 1. Architectural Impact & Overview
Brief explanation of where this feature sits in the codebase architecture.

## 2. Reusable Components & Modules (Reuse-First Check)
> [!IMPORTANT]
> Always reuse existing components before introducing new abstractions!

- **Primitive Components Reused** (from `@/components/ui/`):
  - [x] `Button` (`src/components/ui/button.tsx`)
  - [x] `Input` (`src/components/ui/input.tsx`)
  - [ ] `Dialog` / `Card` ...
- **Shared Business Components Reused** (from `@/components/shared/`):
  - [ ] `Header`, `UserAvatar`, etc.
- **New Components to Create** (Only if strictly needed):
  - `src/components/features/{feature_slug}/...`

## 3. Data Model & Schema Changes
- **Database Tables / Entities Modified/Added**:
  ```prisma
  // Example schema or SQL migration
  model Example {
    id        String   @id @default(uuid())
    createdAt DateTime @default(now())
  }
  ```
- **Migration Plan**: `npx prisma migrate dev` / `alembic upgrade head`.

## 4. API Contracts & Type Definitions (Zod / TypeScript)
```typescript
// Shared contract between FE and BE
import { z } from "zod";

export const ExampleSchema = z.object({
  field: z.string().min(1),
});

export type ExampleInput = z.infer<typeof ExampleSchema>;
```

## 5. Security, Auth & Error Handling Strategy
- Authentication check: Session or JWT bearer validation.
- Authorization: RBAC role requirement (e.g. `user` or `admin`).
- Error codes & standard JSON error responses.

## 6. Testing Strategy
- **Unit Tests**: Schema validation, domain logic.
- **Integration Tests**: API endpoints with mock DB or test container.
- **UI Tests**: Component render, form submit interaction.
