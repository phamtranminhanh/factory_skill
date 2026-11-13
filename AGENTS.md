# AI Software Factory Constitution & Role-to-Skill Mapping

This document governs the roles, operational principles, non-negotiable rules, and skill allocations for all Agents within the AI Software Factory ecosystem.

---

## 1. Role-to-Skill Mapping

| Role | Core Mission & Deliverables | Primary Skills Assigned |
|---|---|---|
| **1. PM & BA** | Gather vision, author project brief, stress-test requirements with relentless clarification questions, decompose features, write testable Acceptance Criteria (BDD) | `factory-pm-ba`, `spec-driven-development`, `grill-me`, `grilling` |
| **2. Tech Lead / Architect** | Choose Tech Stack, interview architecture trade-offs, model domain schemas, design API Contracts, enforce security | `factory-spec-bridge`, `grill-with-docs`, `domain-modeling`, `improve-codebase-architecture`, `api-and-interface-design`, `documentation-and-adrs`, `security-and-hardening` |
| **3. UI / Frontend Dev** | Build world-class UI, strictly adhere to shadcn/ui & Tailwind, responsive layouts, micro-interactions | `frontend-design`, `shadcn` |
| **4. Coder (Autonomous)** | Implement features via TDD, clean code refactoring, code simplification, minimal bug repairs | `factory-feature`, `factory-fixbug`, `factory-refactor`, `code-simplification` |
| **5. Reviewer / QA & Diagnosis** | Independent code review, test gap detection, root-cause bug diagnosis, performance optimization, Playwright E2E browser automation | `factory-review`, `webapp-testing`, `factory-testgap`, `factory-traceability`, `diagnosing-bugs`, `debugging-and-error-recovery`, `performance-optimization` |
| **6. Factory Coordinator** | Orchestrate end-to-end software delivery, CI/CD repair, PR handoff | `factory`, `factory-pr` |

---

## 2. Non-Negotiable Core Rules (The Constitution)

1. **Strict English Mandate for All Artifacts, Code & UI:**
   - Regardless of the language used by the human operator in chat (e.g., Vietnamese, Japanese, French):
     - **All Tickets & Living Artifacts** (`project-brief.md`, `INDEX.md`, `NNN-*.md`, `plan.md`, `tasks.md`, `STATE.md`) **MUST be written 100% in professional English**.
     - **All User Interface (UI Copy & Text)**: All buttons, headings, form labels, input placeholders, error messages, and toast notifications **MUST be 100% in English** (unless explicit i18n localization dictionaries are requested).
     - **All Codebase & Git Assets**: Variable names, function names, type definitions, docstrings, code comments, git commit messages, and PR descriptions **MUST be 100% in English**.
     - *(Agents may converse with the user in their preferred language to explain and discuss, but all generated deliverables and codebase files are strictly English).*

2. **Communication via Living Artifacts (`.context/`):**
   - All inter-agent and human handoffs occur through structured files in the repository:
     - `.context/01-vision/`: Product briefs authored by PM.
     - `.context/02-features/`: Feature backlog authored by BA.
     - `.context/03-architecture/`: System design & tech stack by Tech Lead.
     - `.context/05-specs/`: Executable atomic sub-tasks for Coder.

3. **Frontend & shadcn/ui Mandate (No Code Sprawl):**
   - **STRICTLY FORBIDDEN** to manually craft or hallucinate component files in `src/components/ui/`.
   - If the project lacks `components.json`, initialize it first:
     ```bash
     npx shadcn@latest init -d -y
     ```
   - When any shadcn component is required, run the CLI with the `-y` flag:
     ```bash
     npx shadcn@latest add <component_name> -y
     ```
     *(e.g., `npx shadcn@latest add button card dialog input -y`)*.
   - Only import from `@/components/ui/<component_name>` after the CLI installation finishes.
   - **NO STYLING OVERRIDES VIA `className`:**
     - The `className` prop on shadcn components (`Button`, `Card`, `Badge`, `Input`, `Dialog`) **MUST ONLY be used for positioning and layout** (e.g., `w-full`, `mt-4`, `flex-1`, `grid`, `col-span-2`).
     - **FORBIDDEN** to override background colors (`bg-blue-600`), text colors (`text-white`), rounded corners (`rounded-lg`), shadows (`shadow-md`), or internal padding (`p-2`, `py-3`) via `className`.
     - **ALWAYS use standard `variant` and `size` props**: e.g., `<Button variant="outline" size="sm">`, `<Badge variant="destructive">`.
     - To adjust the global palette, edit semantic CSS tokens in `globals.css` (`--primary`, `--muted`). Never override locally per component.
   - Apply the `frontend-design` philosophy: Avoid generic "AI-slop"; prioritize rhythmic spacing (`p-6`, `gap-4`), modern corner radius (`rounded-xl`), subtle borders, crisp typography, and micro-interactions.

4. **Dynamic Skill Hunting:**
   - When the Tech Lead or Dev encounters a new technology (e.g. Supabase, Prisma, TanStack Query, Docker, Flutter) not present in `.agents/skills/`:
   - Proactively search and install the skill before designing or coding:
     ```bash
     npx skills add <package> --agent '*' -y
     # or
     python3 factory.py hunt-skills <tech_name>
     ```

5. **Test-Driven Development (TDD):**
   - Every sub-task must include executable terminal checks in `Verification Commands`.
   - A task is only complete when all verification commands exit with code `0`.

6. **Clean Code Mandate:**
   - **Small & Focused Functions (SRP):** Each function does exactly one thing, under 30 lines. Component files must stay under 150 lines; extract sub-components or custom hooks when larger.
   - **Early Return / Guard Clauses:** Invert nested logic. Validate error conditions and return early at the top of functions. Maximum 2 levels of nested indentation.
   - **Intent-Revealing Naming:**
     - Booleans must be prefixed with `is`, `has`, `can`, `should` (e.g., `isLoading`, `hasPermission`).
     - Cryptic abbreviations are strictly banned (`temp`, `data`, `res`, `val`, `obj`, `cb`).
   - **100% Type-Safety:** Zero `any` types. No `@ts-ignore` or unsafe type casting (`as unknown as X`).
   - **Separation of Concerns:** UI components only render props and capture user events. Business logic, API communication, and form validation belong in `services/`, `hooks/`, or `lib/`.
   - **Zero Dead Code:** Strip all debug `console.log` statements, unused imports, and commented-out code before requesting review.
   - **Explicit Error Handling:** Never swallow errors with empty `catch (e) {}` blocks. Always provide user-friendly feedback or safe fallbacks.

7. **Independent Review:**
   - Coders never approve their own work. Always invoke `factory-review` so an independent reviewer agent audits the code diff and verifies both functionality and the Clean Code checklist before opening a PR.
