#!/usr/bin/env python3
"""Install the versioned Factory skill suite without overwriting unrelated skills."""
import argparse
import os
from pathlib import Path
import shutil
import tempfile
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, default=Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "skills")
    parser.add_argument("--replace", action="store_true", help="back up and replace existing Factory suite folders")
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    folders = sorted(p for p in source.glob("factory*") if p.is_dir() and (p / "SKILL.md").is_file())
    if not folders or not (source / "factory" / "scripts" / "factory_run.py").is_file():
        raise SystemExit("Incomplete source suite")
    conflicts = [args.destination / p.name for p in folders if (args.destination / p.name).exists()]
    if conflicts and not args.replace:
        raise SystemExit("Existing skills left untouched; inspect before using --replace: " + ", ".join(map(str, conflicts)))
    args.destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="factory-install-", dir=args.destination.parent) as temp:
        staging = Path(temp)
        for p in folders:
            shutil.copytree(p, staging / p.name, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        backup = args.destination.parent / ("factory-backup-" + time.strftime("%Y%m%d-%H%M%S"))
        if conflicts:
            backup.mkdir()
            for p in conflicts:
                shutil.move(str(p), backup / p.name)
            print("Backup:", backup)
        for p in folders:
            shutil.move(str(staging / p.name), args.destination / p.name)
            print("Installed", args.destination / p.name)


if __name__ == "__main__":
    main()
