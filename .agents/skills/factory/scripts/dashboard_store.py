"""Local pointers to Factory evidence runs; no task execution or credentials."""
import hashlib
import json
import os
from pathlib import Path
import tempfile


def registry_root():
    configured = os.environ.get("FACTORY_DASHBOARD_HOME")
    if configured:
        return Path(configured).expanduser().resolve()
    return Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))).expanduser().resolve() / "factory-dashboard"


def run_id(directory):
    return hashlib.sha256(os.fsencode(Path(directory).resolve())).hexdigest()[:24]


def register(directory, registry=None):
    directory = Path(directory).resolve()
    state = json.loads((directory / "state.json").read_text())
    if state.get("schema") != 1 or not isinstance(state.get("repo"), str):
        raise ValueError("Not a Factory evidence run")
    folder = (Path(registry) if registry is not None else registry_root()) / "runs"
    folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    identity = run_id(directory)
    target = folder / (identity + ".json")
    value = json.dumps({"run": str(directory)}, ensure_ascii=False) + "\n"
    if target.exists() and target.read_text() == value:
        return identity
    descriptor, name = tempfile.mkstemp(prefix=".register-", dir=folder)
    try:
        with os.fdopen(descriptor, "w") as output:
            output.write(value)
        os.replace(name, target)
    finally:
        Path(name).unlink(missing_ok=True)
    return identity
