# Factory Bridge: PM/BA to Codex Execution Pipeline

The core orchestration engine bridging the first two stages of the **AI Software Factory**:
1. **PM & BA Stage (`factory-pm-ba`)**: Transforms unstructured app ideas and PRDs into a structured, reviewed feature backlog with testable Acceptance Criteria (BDD format).
2. **Dev & Spec-Kit Stage (`factory-spec-bridge`)**: Converts features into technical specifications (`plan.md` + `tasks.md`) with explicit file targets, executable test verification commands, and component reuse scans before handing off to `codex-factory-skills`.

---

## Directory Architecture

```text
AI Factory/
├── .agents/skills/
│   ├── factory-pm-ba/            # Skill for BA/PM Agent
│   │   └── SKILL.md
│   └── factory-spec-bridge/      # Skill for Tech Lead / Dev Agent
│       └── SKILL.md
│
├── factory-bridge/
│   ├── factory_bridge.py         # Automation CLI (Standard Library only)
│   ├── templates/                # Standardized artifact templates
│   │   ├── project-brief-template.md
│   │   ├── feature-template.md
│   │   ├── plan-template.md
│   │   ├── tasks-template.md
│   │   └── state-template.md
│   └── README.md
│
├── factory_skill/                # Upstream BA feature decomposer
└── codex-factory-skills/         # Downstream autonomous coding runner (factory-feature, review...)
```

---

## 3-Step Execution Playbook

### Step 1: Project Initialization & Feature Backlog (PM & BA)
1. Within Antigravity (or Claude Code), activate `factory-pm-ba` or execute:
   ```bash
   python3 factory-bridge/factory_bridge.py init "my-awesome-app"
   ```
2. The agent generates the `.context/` structure:
   - `.context/01-vision/project-brief.md`: Problem statement, target personas, MVP boundaries.
   - `.context/02-features/INDEX.md`: Master feature table (P0–P3) and dependency DAG.
   - `.context/02-features/NNN-*.md`: Detailed feature specifications with BDD Acceptance Criteria.
   - `.context/STATE.md`: Global pipeline state board.

---

### Step 2: Technical Breakdown via Spec-Kit (Dev Lead)
When a feature is ready for implementation (e.g. `004-register-with-phone-number-and-otp.md`):

1. Activate `factory-spec-bridge` or execute:
   ```bash
   python3 factory-bridge/factory_bridge.py make-spec ".context/02-features/004-register.md"
   ```
2. The folder `.context/05-specs/004-register/` is created, containing:
   - `spec.md`: Extracted business criteria from BA.
   - `plan.md`: Database schemas, API contracts (Zod), and reusable components from `@/components/ui/`.
   - `tasks.md`: Atomic sub-tasks. Each task defines:
     - *Target Files*: Exact paths to create or modify.
     - *Step-by-Step*: Specific implementation guidance.
     - *Verification Commands*: Executable terminal test commands (e.g., `npm test ...`).
     - *Definition of Done*.

3. **Verify Compliance Before Code Execution:**
   ```bash
   python3 factory-bridge/factory_bridge.py validate-spec ".context/05-specs/004-register/tasks.md"
   ```
   *Guarantees no missing verification commands or file targets before agent execution.*

4. **Dev Review (Human Checkpoint):**
   Review `tasks.md`, adjust logic if necessary, and approve (`ready-to-code`).

---

### Step 3: Handoff to `codex-factory-skills` for Autonomous Coding
Export the prompt for a specific sub-task:
```bash
python3 factory-bridge/factory_bridge.py export-prompt ".context/05-specs/004-register/tasks.md" 1
```

Feed this prompt into `codex-factory-skills` (`factory-feature`):
1. Codex receives the task and authors unit tests first (TDD).
2. Implements business logic strictly adhering to Clean Code standards.
3. Executes `Verification Commands` to prove zero regressions.
4. Triggers `factory-review` for independent diff auditing and opens a Pull Request!
