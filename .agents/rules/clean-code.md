# Global Clean Code Guidelines & Architectural Rules

Mandatory coding standards for all AI Coding Agents in this repository.

---

## 0. Strict English Mandate
- **All Code, UI & Artifacts**: Every piece of visible UI copy (buttons, labels, placeholders, toasts, banners, errors), identifier names, schemas, inline comments, git commit messages, PR descriptions, and specification files (`.context/`) **MUST BE 100% IN ENGLISH**.
- Even if the user communicates in Vietnamese or any other language during conversation, all files committed to the repository **ARE ALWAYS WRITTEN IN ENGLISH**.

## 1. Single Responsibility Principle (SRP) & Function Sizing
- Every function/method must do **EXACTLY ONE THING** and do it well.
- Target function length: **Under 25 - 30 lines**.
- UI Component files: **Under 150 lines**. When exceeded, components must be decomposed into sub-components or custom hooks in dedicated subdirectories.

## 2. Guard Clauses & Early Return (Avoid Pyramid of Doom)
- **Strictly forbidden** to nest `if-else` blocks more than 2 levels deep.
- Always validate error conditions, missing parameters, and boundary edge cases at the very beginning of the function and return immediately:
  ```typescript
  // ❌ BAD:
  function handleOrder(user, cart) {
    if (user) {
      if (cart && cart.items.length > 0) {
        // ... 50 lines of deeply nested logic
      }
    }
  }

  // ✅ GOOD:
  function handleOrder(user: User, cart: Cart) {
    if (!user) throw new UnauthorizedError();
    if (!cart?.items?.length) return { success: false, reason: "EMPTY_CART" };

    // Flat, readable core business execution
  }
  ```

## 3. Intent-Revealing Naming
- **Identifiers must be self-documenting**:
  - Boolean variables: Must be prefixed with `is`, `has`, `can`, `should` (e.g., `isLoading`, `hasPermission`, `canCheckout`).
  - Action functions: Must begin with active verbs (e.g., `calculateTotal`, `fetchUserProfile`, `verifyPassword`).
- **Meaningless abbreviations are strictly banned**: Do not use `temp`, `data`, `res`, `val`, `cb`, `obj`, `item2`.
- Single-letter variables are forbidden (except for standard loop indices `i, j`).

## 4. Strict Type-Safety (Zero `any`)
- **100% ban on the `any` type** in TypeScript.
- Never use `@ts-ignore` or `@ts-nocheck` to bypass compilation errors.
- Every public function, API route, and server action must declare explicit parameter and return types.
- Use **Zod** to validate all external and user inputs before passing them into domain services.

## 5. Separation of Concerns
- **UI Layer**: Responsible only for rendering props and handling user interactions.
- **Domain/Service Layer**: All business formulas, validation logic, and database operations belong in `services/`, `lib/`, or Custom Hooks.
- Never write raw SQL / Prisma queries directly inside React JSX components.

## 6. Explicit Error Handling
- **Never swallow errors**: Empty `catch (error) {}` blocks are strictly forbidden.
- Every error must either:
  1. Be logged with full execution context (function name, input arguments).
  2. Be surfaced to the end user as an informative, safe, and friendly error message.

## 7. Zero Dead Code
- Clean up all:
  - Temporary debug `console.log` statements.
  - Commented-out dead code (`// const oldCode = ...`).
  - Unused imports, unused variables, and deprecated dependencies.
- Follow **DRY (Don't Repeat Yourself)**: Avoid duplicating identical logic across multiple call sites.
