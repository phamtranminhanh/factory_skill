#!/usr/bin/env python3
"""
Factory Bridge CLI: Connecting PM/BA feature breakdowns to Developer execution specs.
Uses standard library only.
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import subprocess
import shutil

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"


def read_template(name: str) -> str:
    path = TEMPLATES_DIR / name
    if not path.is_file():
        raise FileNotFoundError(f"Template not found: {path}")
    return path.read_text(encoding="utf-8")


def cmd_init(args):
    app_name = args.app_name.strip()
    target_dir = Path(args.target).resolve()
    context_dir = target_dir / ".context"

    print(f"🚀 Initializing AI Software Factory structure for: '{app_name}'")
    print(f"   Target directory: {target_dir}")

    # Create directories
    for sub in ["01-vision", "02-features", "03-architecture", "04-ui", "05-specs"]:
        (context_dir / sub).mkdir(parents=True, exist_ok=True)

    # 1. Project Brief
    brief_file = context_dir / "01-vision" / "project-brief.md"
    if not brief_file.exists() or args.force:
        tpl = read_template("project-brief-template.md")
        brief_file.write_text(tpl.replace("{app_name}", app_name), encoding="utf-8")
        print(f"   ✓ Created {brief_file.relative_to(target_dir)}")

    # 2. State Board
    state_file = context_dir / "STATE.md"
    if not state_file.exists() or args.force:
        tpl = read_template("state-template.md")
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        state_file.write_text(tpl.replace("{app_name}", app_name).replace("{timestamp}", ts), encoding="utf-8")
        print(f"   ✓ Created {state_file.relative_to(target_dir)}")

    # 3. Features INDEX placeholder
    features_index = context_dir / "02-features" / "INDEX.md"
    if not features_index.exists() or args.force:
        features_index.write_text(
            f"# Feature Index: {app_name}\n\n| ID | Feature | Priority | Area | Depends On |\n|---|---|---|---|---|\n| 001 | Project Setup & CI/CD | P0 | Foundation | none |\n",
            encoding="utf-8",
        )
        print(f"   ✓ Created {features_index.relative_to(target_dir)}")

    # 4. Tech Stack placeholder
    tech_stack = context_dir / "03-architecture" / "TECH_STACK.md"
    if not tech_stack.exists() or args.force:
        tech_stack.write_text(
            f"# Tech Stack & Architecture: {app_name}\n\n- **Framework**: Next.js 15 (App Router)\n- **Language**: TypeScript\n- **Styling**: Tailwind CSS\n- **UI Components**: shadcn/ui\n- **Database**: PostgreSQL with Prisma ORM\n- **Testing**: Vitest + Playwright\n",
            encoding="utf-8",
        )
        print(f"   ✓ Created {tech_stack.relative_to(target_dir)}")

    print(f"\n✅ Factory initialized successfully. Next step: run BA Feature Breakdown.")


def parse_feature_file(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    filename = file_path.stem  # e.g. 004-register-with-phone-number-and-otp

    # Extract ID and Title from filename or header
    id_match = re.match(r"^(\d{3})-(.+)$", filename)
    if id_match:
        feat_id = id_match.group(1)
        feat_slug = id_match.group(2)
    else:
        feat_id = "000"
        feat_slug = filename

    # Extract title from first markdown header
    header_match = re.search(r"^#\s*(?:\[\d+\])?\s*(.+)$", content, re.MULTILINE)
    title = header_match.group(1).strip() if header_match else feat_slug.replace("-", " ").title()

    # Extract priority
    prio_match = re.search(r"\|\s*Priority\s*\|\s*(P[0-3])", content, re.IGNORECASE)
    priority = prio_match.group(1).upper() if prio_match else "P1"

    # Extract area
    area_match = re.search(r"\|\s*Area\s*\|\s*([^|\n]+)", content, re.IGNORECASE)
    area = area_match.group(1).strip() if area_match else "Core"

    # Extract dependencies
    dep_match = re.search(r"\|\s*Depends on\s*\|\s*([^|\n]+)", content, re.IGNORECASE)
    depends_on = dep_match.group(1).strip() if dep_match else "none"

    return {
        "id": feat_id,
        "slug": feat_slug,
        "title": title,
        "priority": priority,
        "area": area,
        "depends_on": depends_on,
        "content": content,
    }


def cmd_make_spec(args):
    feature_path = Path(args.feature_file).resolve()
    if not feature_path.is_file():
        raise SystemExit(f"Error: Feature file not found at {feature_path}")

    feat = parse_feature_file(feature_path)
    output_base = Path(args.output_dir).resolve() if args.output_dir else feature_path.parent.parent / "05-specs"
    spec_dir = output_base / f"{feat['id']}-{feat['slug']}"
    spec_dir.mkdir(parents=True, exist_ok=True)

    print(f"📋 Generating Technical Specification for [{feat['id']}] {feat['title']}")
    print(f"   Target specs directory: {spec_dir}")

    # 1. spec.md (Business spec)
    spec_file = spec_dir / "spec.md"
    spec_file.write_text(feat["content"], encoding="utf-8")
    print(f"   ✓ Created {spec_file.name}")

    # 2. plan.md (Technical plan)
    plan_file = spec_dir / "plan.md"
    if not plan_file.exists() or args.force:
        tpl_plan = read_template("plan-template.md")
        rendered_plan = tpl_plan.replace("{id}", feat["id"]).replace("{title}", feat["title"]).replace("{feature_slug}", feat["slug"])
        plan_file.write_text(rendered_plan, encoding="utf-8")
        print(f"   ✓ Created {plan_file.name}")

    # 3. tasks.md (Atomic Sub-tasks for Developer)
    tasks_file = spec_dir / "tasks.md"
    if not tasks_file.exists() or args.force:
        tpl_tasks = read_template("tasks-template.md")
        rendered_tasks = (
            tpl_tasks.replace("{id}", feat["id"])
            .replace("{title}", feat["title"])
            .replace("{feature_slug}", feat["slug"])
            .replace("{total_tasks}", "3")
            .replace("{task_01_title}", f"Data Model & API Contracts for {feat['title']}")
            .replace("{task_02_title}", f"Backend Endpoint & Domain Service for {feat['title']}")
            .replace("{task_03_title}", f"Frontend UI Integration & Verification for {feat['title']}")
        )
        tasks_file.write_text(rendered_tasks, encoding="utf-8")
        print(f"   ✓ Created {tasks_file.name}")

    print(f"\n✅ Spec packet generated at: {spec_dir}")
    print(f"👉 Next step: Dev Lead reviews and refines 'plan.md' and 'tasks.md' before execution.")


def cmd_validate_spec(args):
    tasks_file = Path(args.tasks_file).resolve()
    if not tasks_file.is_file():
        raise SystemExit(f"Error: tasks.md not found at {tasks_file}")

    content = tasks_file.read_text(encoding="utf-8")
    subtasks = re.split(r"(?=###\s*\[Sub-Task\s*\d+\])", content)
    subtasks = [st.strip() for st in subtasks if st.strip().startswith("### [Sub-Task")]

    if not subtasks:
        print(f"❌ Error: No sub-tasks found matching '### [Sub-Task NN]' pattern in {tasks_file}")
        sys.exit(1)

    print(f"🔍 Validating {len(subtasks)} sub-task(s) in {tasks_file.name}...")

    all_passed = True
    required_sections = [
        ("Target Files", r"Target Files to Create\s*/\s*Modify"),
        ("Step-by-Step Instructions", r"Step-by-Step Instructions"),
        ("Verification Commands", r"Verification Commands"),
        ("Definition of Done", r"Definition of Done"),
    ]

    for idx, st in enumerate(subtasks, start=1):
        header_match = re.match(r"###\s*\[Sub-Task\s*(\d+)\]:\s*(.+)", st)
        title = header_match.group(2) if header_match else f"Task {idx}"
        print(f"\n   Testing [Sub-Task {idx}]: {title}")

        for sec_name, pattern in required_sections:
            if not re.search(pattern, st, re.IGNORECASE):
                print(f"     ❌ Missing required section: '{sec_name}'")
                all_passed = False
            else:
                print(f"     ✓ Section '{sec_name}' present")

    if all_passed:
        print(f"\n🎉 ALL CHECKS PASSED: Tasks are compliant and ready for autonomous Developer execution!")
        sys.exit(0)
    else:
        print(f"\n⚠️  VALIDATION FAILED: Please fix the missing sections above before running with Developer Agent.")
        sys.exit(1)


def cmd_hunt_skills(args):
    query = args.query.strip()
    print(f"🔎 Hunting skills online for tech stack: '{query}'...")

    # Run npx skills find
    try:
        proc = subprocess.run(
            ["npx", "skills", "find", query],
            capture_output=True,
            text=True,
            timeout=15,
        )
        output = proc.stdout
    except Exception as e:
        print(f"❌ Failed to run skills search: {e}")
        return

    # Extract matches (pattern: package@skill or package)
    matches = re.findall(r"([a-zA-Z0-9_\-\./]+@[a-zA-Z0-9_\-\./:]+)", output)
    if not matches:
        # Fallback pattern: e.g. vercel-labs/agent-skills
        matches = re.findall(r"([a-zA-Z0-9_\-]+/[a-zA-Z0-9_\-]+)", output)

    if not matches:
        print(f"⚠️ No specific skills found on skills.sh for '{query}'.")
        return

    # Take unique top matches
    unique_matches = []
    ignored = {"owner/repo", "npx", "package"}
    for m in matches:
        pkg = m.split("@")[0].strip()
        if pkg not in unique_matches and pkg not in ignored and "/" in pkg and not pkg.startswith("npx"):
            unique_matches.append(pkg)

    print(f"🎯 Found top relevant skill packages:")
    for idx, m in enumerate(unique_matches[:3], start=1):
        print(f"   [{idx}] {m}")

    top_pkg = unique_matches[0]
    print(f"\n📦 Automatically installing top package: '{top_pkg}' for all agents...")

    try:
        install_proc = subprocess.run(
            ["npx", "skills", "add", top_pkg, "--agent", "*", "-y"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        print(install_proc.stdout)

        # Mirror newly installed skills to .gemini/skills
        agents_skills_dir = Path(".agents/skills")
        gemini_skills_dir = Path(".gemini/skills")
        if agents_skills_dir.exists():
            gemini_skills_dir.mkdir(parents=True, exist_ok=True)
            for item in agents_skills_dir.iterdir():
                if item.is_dir() and (item / "SKILL.md").exists():
                    dest = gemini_skills_dir / item.name
                    if not dest.exists():
                        shutil.copytree(item, dest)
                        print(f"   ✓ Synced {item.name} to .gemini/skills")

        print(f"\n🎉 Skill package '{top_pkg}' is now active and ready for your agents!")
    except Exception as e:
        print(f"❌ Installation failed: {e}")


def cmd_export_prompt(args):
    tasks_file = Path(args.tasks_file).resolve()
    if not tasks_file.is_file():
        raise SystemExit(f"Error: tasks.md not found at {tasks_file}")

    content = tasks_file.read_text(encoding="utf-8")
    subtasks = re.split(r"(?=###\s*\[Sub-Task\s*\d+\])", content)
    subtasks = [st.strip() for st in subtasks if st.strip().startswith("### [Sub-Task")]

    target_idx = args.subtask_num
    if target_idx < 1 or target_idx > len(subtasks):
        raise SystemExit(f"Error: Invalid subtask number {target_idx}. Total subtasks: {len(subtasks)}")

    selected_task = subtasks[target_idx - 1]

    prompt = f"""You are the Factory Feature Developer.
Execute the following sub-task strictly adhering to the Verification Commands and Definition of Done.

{selected_task}

Rules:
1. Only create or modify the designated Target Files.
2. Run the specified Verification Commands in the terminal to confirm correctness.
3. Ensure all tests exit with code 0 before concluding.
"""
    print("=" * 60)
    print(f"PROMPT FOR DEVELOPER / FACTORY-FEATURE (Sub-Task {target_idx}):")
    print("=" * 60)
    print(prompt)


def main():
    parser = argparse.ArgumentParser(description="Factory Bridge CLI: Connecting PM/BA breakdowns to Developer execution.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # init
    p_init = subparsers.add_parser("init", help="Initialize .context/ structure for an app")
    p_init.add_argument("app_name", help="Name of the application")
    p_init.add_argument("--target", default=".", help="Target project root directory (default: current)")
    p_init.add_argument("--force", action="store_true", help="Overwrite existing files")
    p_init.set_defaults(func=cmd_init)

    # make-spec
    p_spec = subparsers.add_parser("make-spec", help="Decompose a BA feature file into a Technical Spec packet")
    p_spec.add_argument("feature_file", help="Path to the NNN-feature.md file")
    p_spec.add_argument("--output-dir", help="Destination specs directory (default: .context/05-specs)")
    p_spec.add_argument("--force", action="store_true", help="Overwrite existing spec files")
    p_spec.set_defaults(func=cmd_make_spec)

    # validate-spec
    p_val = subparsers.add_parser("validate-spec", help="Validate tasks.md for Developer compliance")
    p_val.add_argument("tasks_file", help="Path to tasks.md")
    p_val.set_defaults(func=cmd_validate_spec)

    # export-prompt
    p_exp = subparsers.add_parser("export-prompt", help="Export a specific subtask as an executable prompt for Developer Agent")
    p_exp.add_argument("tasks_file", help="Path to tasks.md")
    p_exp.add_argument("subtask_num", type=int, help="Sub-task index (1-based)")
    p_exp.set_defaults(func=cmd_export_prompt)

    # hunt-skills
    p_hunt = subparsers.add_parser("hunt-skills", help="Proactively search and install skills online for any tech stack")
    p_hunt.add_argument("query", help="Name of tech stack / framework (e.g. prisma, flutter, docker, tanstack)")
    p_hunt.set_defaults(func=cmd_hunt_skills)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
