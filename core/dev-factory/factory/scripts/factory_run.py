#!/usr/bin/env python3
"""Local evidence ledger for the Factory skills. No model, network or daemon.

This is an audit helper for a cooperative coordinator, not a security boundary.
Commands are explicit argv arrays; evidence never claims to prove model independence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import stat
import subprocess
import sys
import tempfile
import time
import uuid
from dataclasses import asdict

from vendor import tamper_guard
from dashboard_store import register as register_dashboard

KINDS = ("feature", "bugfix", "ci_fix", "traceability", "test_gap", "investigation",
         "code_review", "design_doc", "refactor", "docs")
REPORT_ONLY = {"investigation", "code_review", "design_doc"}
BLOCKING = {"critical", "high", "medium"}
MAX_LOG = 2 * 1024 * 1024


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE)


def root(path):
    return Path(os.fsdecode(git(path, "rev-parse", "--show-toplevel")).strip()).resolve()


def sha(repo, ref="HEAD"):
    return git(repo, "rev-parse", "--verify", ref + "^{commit}").decode().strip()


def paths(repo):
    return sorted(set(os.fsdecode(p) for p in git(
        repo, "ls-files", "-z", "--cached", "--others", "--exclude-standard").split(b"\0") if p))


def safe_path(repo, relative):
    p = Path(relative)
    if p.is_absolute() or ".." in p.parts or ".git" in p.parts:
        raise ValueError(f"path must stay within the repository: {relative}")
    if p == Path("."):
        return repo
    resolved_parent = (repo / p).parent.resolve()
    if not resolved_parent.is_relative_to(repo):
        raise ValueError(f"path escapes through a symlink: {relative}")
    return repo / p


def snapshot(repo):
    digest = hashlib.sha256()
    for rel in paths(repo):
        p = safe_path(repo, rel)
        if p.is_symlink():
            mode, content = "symlink", os.fsencode(os.readlink(p))
        elif p.is_file():
            mode = "executable" if p.stat().st_mode & stat.S_IXUSR else "file"
            content = p.read_bytes()
        elif not p.exists():
            mode, content = "deleted", b""
        else:
            raise ValueError(f"unsupported tracked directory/submodule: {rel}; verify each repo separately")
        digest.update(os.fsencode(rel) + b"\0" + mode.encode() + b"\0")
        digest.update(hashlib.sha256(content).digest())
    return {"fingerprint": digest.hexdigest(), "head": sha(repo),
            "clean": not bool(git(repo, "status", "--porcelain", "--untracked-files=normal"))}


def write_json(path, data):
    path = Path(path)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    tmp.replace(path)


def read_json(path):
    return json.loads(Path(path).read_text())


def load(run):
    directory = Path(run).resolve()
    data = read_json(directory / "state.json")
    if data.get("schema") != 1:
        raise ValueError("unknown run schema")
    repo = root(data["repo"])
    if str(repo) != data["repo"]:
        raise ValueError("run repository moved; create a new run")
    return directory, data, repo


def save(directory, data, event):
    data["updated_at"] = time.time()
    write_json(directory / "state.json", data)
    with (directory / "events.jsonl").open("a") as out:
        out.write(json.dumps({"at": data["updated_at"], "event": event,
                              "round": data["round"]}) + "\n")
    try:
        register_dashboard(directory)
    except (OSError, ValueError) as exc:
        print(f"Dashboard registration unavailable: {exc}", file=sys.stderr)


def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))


def artifact(directory, label, value):
    name = f"{label}-{uuid.uuid4().hex[:8]}.json"
    write_json(directory / name, value)
    return name


def active(data):
    if data["phase"] != "working":
        raise ValueError("begin a round first; a blocked run must be explicitly resumed")
    if time.time() > data["deadline"]:
        raise ValueError("run deadline exceeded; report budget_exhausted, do not silently extend")


def positive(value):
    n = int(value)
    if n <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return n


def run_process(command, cwd, directory, timeout, label):
    if not isinstance(command, list) or not command or not all(isinstance(x, str) and x for x in command):
        raise ValueError("command must be a nonempty argv array")
    log = directory / f"{label}-{uuid.uuid4().hex[:8]}.log"
    started = time.time()
    env = dict(os.environ)
    # Do not let a caller's Python path silently import the original checkout.
    env["PYTHONPATH"] = os.pathsep.join([str(cwd / "src"), str(cwd)])
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONNOUSERSITE"] = "1"
    timed_out = False
    try:
        with tempfile.TemporaryFile() as capture:
            proc = subprocess.Popen(command, cwd=cwd, env=env, stdout=capture,
                                    stderr=subprocess.STDOUT, start_new_session=True)
            try:
                code = proc.wait(timeout=timeout)
            except (subprocess.TimeoutExpired, KeyboardInterrupt):
                timed_out = True
                os.killpg(proc.pid, signal.SIGKILL)
                code = proc.wait()
            capture.seek(0, 2)
            total = capture.tell()
            capture.seek(max(0, total - MAX_LOG))
            output = capture.read().decode("utf-8", errors="replace")
            log.write_text(("[earlier output truncated]\n" if total > MAX_LOG else "") + output)
    except OSError as exc:
        code, output = None, str(exc)
        log.write_text(output)
    return {"argv": command, "cwd": str(cwd), "exit_code": code,
            "timed_out": timed_out, "seconds": round(time.time() - started, 3),
            "log": log.name, "status": "pass" if code == 0 and not timed_out else "fail"}, output


def test_snapshots(repo, base):
    before = {}
    for record in git(repo, "ls-tree", "-r", "-z", base).split(b"\0"):
        if not record:
            continue
        meta, rawpath = record.split(b"\t", 1)
        rel = os.fsdecode(rawpath)
        if meta.split()[1] == b"blob" and tamper_guard.is_test_file(rel):
            before[rel] = git(repo, "cat-file", "blob", meta.split()[2].decode()).decode("utf-8", errors="replace")
    after = {}
    for rel in paths(repo):
        if tamper_guard.is_test_file(rel):
            p = safe_path(repo, rel)
            if p.is_symlink():
                raise ValueError(f"test symlink requires manual inspection: {rel}")
            if p.is_file():
                after[rel] = p.read_text(errors="replace")
    return before, after


def cmd_init(a):
    repo = root(a.repo)
    current = snapshot(repo)
    if a.kind not in REPORT_ONLY and not current["clean"]:
        raise ValueError("mutating tasks need a clean baseline; preserve user changes and use a separate worktree")
    criteria = read_json(a.criteria)
    if not isinstance(criteria, list) or not criteria or not all(isinstance(x, str) and x.strip() for x in criteria):
        raise ValueError("criteria file must be a nonempty JSON array of acceptance-criterion strings")
    base = sha(repo, a.base)
    common = Path(os.fsdecode(git(repo, "rev-parse", "--git-common-dir")).strip())
    if not common.is_absolute():
        common = repo / common
    directory = common.resolve() / "factory-runs" / (time.strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6])
    directory.mkdir(parents=True, mode=0o700)
    checks = a.checks.split(",") if a.checks is not None else ([] if a.kind in REPORT_ONLY | {"docs"} else ["test"])
    data = {"schema": 1, "repo": str(repo), "kind": a.kind, "title": a.title,
            "base": base, "initial": current, "criteria": {f"C{i+1}": s for i, s in enumerate(criteria)},
            "required_checks": [x.strip() for x in checks if x.strip()], "round": 0,
            "max_rounds": a.max_rounds, "deadline": time.time() + 60 * a.minutes,
            "phase": "intake", "checks": {}, "reviews": [], "created_at": time.time()}
    save(directory, data, "created")
    emit({"run": str(directory), **data})


def cmd_plan(a):
    directory, data, _ = load(a.run)
    plan = read_json(a.file)
    if not isinstance(plan, dict) or not str(plan.get("approach", "")).strip():
        raise ValueError("plan requires an approach (or explicit trivial-task rationale)")
    if set(plan.get("criteria", [])) != set(data["criteria"]):
        raise ValueError("plan must name every criterion id exactly")
    data["plan"] = artifact(directory, "plan", plan)
    save(directory, data, "plan_recorded")
    emit({"plan": data["plan"]})


def cmd_begin(a):
    directory, data, _ = load(a.run)
    if data["phase"] == "blocked":
        raise ValueError("resume the blocker explicitly before beginning another round")
    if not data.get("plan"):
        raise ValueError("record the plan before implementation/review")
    if data["round"] >= data["max_rounds"] or time.time() >= data["deadline"]:
        raise ValueError("budget exhausted; stop and explain what remains")
    data["round"] += 1
    data["phase"] = "working"
    save(directory, data, "round_started")
    emit({"round": data["round"], "max_rounds": data["max_rounds"]})


def cmd_check(a):
    directory, data, repo = load(a.run)
    active(data)
    cwd = safe_path(repo, a.cwd).resolve()
    if not cwd.is_dir() or not cwd.is_relative_to(repo):
        raise ValueError("check cwd must be a directory inside the repo")
    before = snapshot(repo)
    command = a.argv[1:] if a.argv[:1] == ["--"] else a.argv
    result, _ = run_process(command, cwd, directory, min(a.timeout, max(1, data["deadline"] - time.time())), a.name)
    after = snapshot(repo)
    result.update(fingerprint=before["fingerprint"], head=before["head"], round=data["round"])
    if before["fingerprint"] != after["fingerprint"]:
        result["status"] = "stale"
        result["reason"] = "command changed the candidate; inspect the change and rerun"
    data["checks"][a.name] = artifact(directory, "check", result)
    save(directory, data, "check_recorded")
    emit(result)
    return 0 if result["status"] == "pass" else 1


def cmd_tamper(a):
    directory, data, repo = load(a.run)
    active(data)
    snap = snapshot(repo)
    before, after = test_snapshots(repo, data["base"])
    result = asdict(tamper_guard.check(before, after))
    result.update(fingerprint=snap["fingerprint"], status="flagged" if result["tampered"] else "pass")
    if snapshot(repo)["fingerprint"] != snap["fingerprint"]:
        raise ValueError("candidate changed during tamper inspection")
    data["tamper"] = artifact(directory, "tamper", result)
    save(directory, data, "tamper_recorded")
    emit(result)
    return 1 if result["tampered"] else 0


def cmd_review(a):
    directory, data, repo = load(a.run)
    active(data)
    report = read_json(a.file)
    if not isinstance(report, dict):
        raise ValueError("review must be a JSON object")
    current = snapshot(repo)
    if report.get("fingerprint") != current["fingerprint"]:
        raise ValueError("review targets stale or modified code; discard verdict and re-review")
    if data["kind"] in REPORT_ONLY:
        if not data.get("deliverable") or report.get("deliverable_sha256") != data["deliverable"]["sha256"]:
            raise ValueError("report-only review must target the recorded deliverable hash")
    if report.get("independent") is not True or not report.get("reviewer_id"):
        raise ValueError("record an independent reviewer session; same-session self-review is advisory")
    if report.get("verdict") not in ("pass", "fail"):
        raise ValueError("review must explicitly say pass or fail")
    rows = report.get("criteria")
    if not isinstance(rows, list) or len(rows) != len(data["criteria"]) or {r.get("id") for r in rows} != set(data["criteria"]):
        raise ValueError("review needs exactly one result for every acceptance criterion")
    for row in rows:
        if row.get("status") not in ("met", "not_met", "unknown") or not str(row.get("evidence", "")).strip():
            raise ValueError("each criterion needs status and concrete evidence")
    findings = report.get("findings")
    if not isinstance(findings, list):
        raise ValueError("review must provide a findings array, empty only if none found")
    for item in findings:
        if item.get("severity") not in BLOCKING | {"low", "nit"} or not item.get("evidence"):
            raise ValueError("finding needs known severity and evidence")
        rel, line = item.get("file"), item.get("line")
        if rel:
            p = safe_path(repo, rel)
            if p.is_symlink() or not p.is_file():
                raise ValueError(f"invalid finding citation: {rel}; cite a current source or use an artifact reference")
            if not isinstance(line, int) or isinstance(line, bool) or not 1 <= line <= len(p.read_text(errors="replace").splitlines()):
                raise ValueError(f"invalid line citation: {rel}:{line}")
        elif not item.get("artifact"):
            raise ValueError("finding needs a source file/line or an evidence-artifact reference")
    report["status"] = "pass" if (report["verdict"] == "pass" and all(r["status"] == "met" for r in rows)
        and not any(f["severity"] in BLOCKING for f in findings) and report.get("goal_reachable") is not False) else "fail"
    data["reviews"].append(artifact(directory, "review", report))
    save(directory, data, "review_recorded")
    emit(report)
    return 0 if report["status"] == "pass" else 1


def cmd_adjudicate(a):
    directory, data, repo = load(a.run)
    active(data)
    report = read_json(a.file)
    tamper = read_json(directory / data["tamper"])
    if report.get("fingerprint") != snapshot(repo)["fingerprint"] or report.get("fingerprint") != tamper["fingerprint"]:
        raise ValueError("stale tamper adjudication")
    if not report.get("reviewer_id") or report.get("independent") is not True:
        raise ValueError("independent adjudication required")
    if report.get("verdict") not in ("legitimate", "tampering", "cannot_decide"):
        raise ValueError("unknown tamper verdict")
    decisions = report.get("decisions", [])
    if report["verdict"] == "legitimate":
        if {d.get("reason") for d in decisions} != set(tamper["reasons"]):
            raise ValueError("justify every exact flagged reason")
        if any(d.get("criterion") not in data["criteria"] or not d.get("evidence") for d in decisions):
            raise ValueError("each justification must cite a criterion and evidence")
    data["adjudication"] = artifact(directory, "adjudication", report)
    save(directory, data, "tamper_adjudicated")
    emit(report)
    return 0 if report["verdict"] == "legitimate" else 1


def cmd_repro(a):
    directory, data, repo = load(a.run)
    active(data)
    manifest = read_json(a.manifest)
    files, command = manifest.get("files"), manifest.get("argv")
    if not isinstance(files, list) or not files or not all(isinstance(p, str) and tamper_guard.is_test_file(p) for p in files):
        raise ValueError("manifest files must be an explicit nonempty list of test/test-support paths")
    pattern = manifest.get("failure_pattern")
    if not isinstance(pattern, str) or not pattern.strip():
        raise ValueError("supply the expected behavioral failure_pattern; any nonzero exit is not proof")
    expected = re.compile(pattern)
    if not isinstance(command, list) or not command:
        raise ValueError("manifest requires test argv")
    for arg in command[1:]:
        if str(repo) in arg:
            raise ValueError("test arguments must not point back into the candidate checkout")
    snap = snapshot(repo)
    temp = Path(tempfile.mkdtemp(prefix="factory-repro-")).resolve()
    base = temp / "base"
    result = {"fingerprint": snap["fingerprint"], "base": data["base"], "files": files, "status": "error"}
    def remaining_timeout():
        remaining = data["deadline"] - time.time()
        if remaining <= 0:
            raise ValueError("run deadline exceeded during reproduction")
        return min(a.timeout, remaining)

    try:
        git(repo, "worktree", "add", "--detach", str(base), data["base"])
        cwdrel = manifest.get("cwd", ".")
        basecwd = safe_path(base, cwdrel).resolve()
        for setup in manifest.get("setup_argv", []):
            receipt, _ = run_process(setup, basecwd, directory, remaining_timeout(), "repro-setup")
            if receipt["status"] != "pass":
                raise ValueError("base setup failed; inspect " + receipt["log"])
        if not snapshot(base)["clean"]:
            raise ValueError("base setup altered source files; cannot claim to test the original base")
        for rel in files:
            source, dest = safe_path(repo, rel), safe_path(base, rel)
            if source.is_symlink() or not source.is_file() or dest.is_symlink():
                raise ValueError(f"repro input must be a regular test file: {rel}")
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(source.read_bytes())
        old, oldtext = run_process(command, basecwd, directory, remaining_timeout(), "repro-before")
        result["before"] = old
        new, _ = run_process(command, safe_path(repo, cwdrel).resolve(), directory, remaining_timeout(), "repro-after")
        result.update(before=old, after=new)
        infra = re.search(r"ModuleNotFoundError|ImportError|SyntaxError|ERROR collecting|no tests ran|command not found", oldtext)
        genuine_red = old["exit_code"] is not None and old["exit_code"] > 0 and not old["timed_out"] and bool(expected.search(oldtext)) and not infra
        result["status"] = "pass" if genuine_red and new["status"] == "pass" else "fail"
        result["expected_failure_matched"] = bool(genuine_red)
        if old["timed_out"] or old["exit_code"] is None or infra:
            result["status"] = "error"
        if snapshot(repo)["fingerprint"] != snap["fingerprint"]:
            result["status"] = "stale"
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        result["reason"] = str(exc)
    finally:
        if base.exists():
            try:
                git(repo, "worktree", "remove", "--force", str(base))
            except subprocess.SubprocessError:
                result["cleanup_pending"] = str(base)
        try:
            temp.rmdir()
        except OSError:
            pass
    data["repro"] = artifact(directory, "repro", result)
    save(directory, data, "repro_recorded")
    emit(result)
    return 0 if result["status"] == "pass" else 1


def cmd_block(a):
    directory, data, _ = load(a.run)
    data["phase"] = "blocked"
    data["blocker"] = {"category": a.category, "reason": a.reason, "question": a.question,
                       "resume_condition": a.resume_condition}
    save(directory, data, "blocked")
    emit(data["blocker"])


def cmd_deliverable(a):
    directory, data, _ = load(a.run)
    active(data)
    content = Path(a.file).read_bytes()
    if not content.strip():
        raise ValueError("deliverable must not be empty")
    name = "deliverable-" + uuid.uuid4().hex[:8] + ".txt"
    (directory / name).write_bytes(content)
    data["deliverable"] = {"file": name, "sha256": hashlib.sha256(content).hexdigest()}
    save(directory, data, "deliverable_recorded")
    emit(data["deliverable"])


def cmd_resume(a):
    directory, data, _ = load(a.run)
    if data["phase"] != "blocked":
        raise ValueError("run is not blocked")
    data["resume_answer"] = a.answer
    if a.extra_rounds or a.extend_minutes:
        if not a.authorization:
            raise ValueError("record the user's authorization before increasing bounds")
        data["budget_authorization"] = a.authorization
        data["max_rounds"] += a.extra_rounds or 0
        if a.extend_minutes:
            data["deadline"] = max(time.time(), data["deadline"]) + 60 * a.extend_minutes
    data["phase"] = "planned"
    save(directory, data, "resumed")
    emit({"phase": data["phase"], "answer": a.answer})


def cmd_gate(a):
    directory, data, repo = load(a.run)
    current = snapshot(repo)
    problems = []
    fp = current["fingerprint"]

    def evidence(key, label):
        name = data.get(key)
        if not name:
            problems.append(label + ": NOT RUN")
            return None
        value = read_json(directory / name)
        if value.get("fingerprint") != fp:
            problems.append(label + ": stale candidate")
        return value

    if data["phase"] == "blocked":
        problems.append("run is blocked")
    if data["kind"] in REPORT_ONLY:
        if fp != data["initial"]["fingerprint"]:
            problems.append("report-only run changed repository content")
        delivery = data.get("deliverable")
        if not delivery or hashlib.sha256((directory / delivery["file"]).read_bytes()).hexdigest() != delivery["sha256"]:
            problems.append("report deliverable missing or changed")
    if not data.get("plan"):
        problems.append("plan missing")
    for name in data["required_checks"]:
        key = data["checks"].get(name)
        if not key:
            problems.append(name + ": NOT RUN")
            continue
        value = read_json(directory / key)
        if value.get("fingerprint") != fp or value.get("status") != "pass":
            problems.append(name + ": failed or stale")
    if data["kind"] not in REPORT_ONLY:
        tamper = evidence("tamper", "tamper")
        if tamper and tamper.get("tampered"):
            adj = evidence("adjudication", "tamper adjudication")
            if not adj or adj.get("verdict") != "legitimate":
                problems.append("test tampering not justified")
    if data["kind"] == "bugfix":
        repro = evidence("repro", "reproduction")
        if repro and repro.get("status") != "pass":
            problems.append("red-before/green-after not proven")
    if not data["reviews"]:
        problems.append("independent review: NOT RUN")
    else:
        review = read_json(directory / data["reviews"][-1])
        if review.get("fingerprint") != fp or review.get("status") != "pass":
            problems.append("independent review failed or stale")
        if data["kind"] in REPORT_ONLY and review.get("deliverable_sha256") != (data.get("deliverable") or {}).get("sha256"):
            problems.append("review targets a different report deliverable")
    result = {"ready": not problems, "kind": data["kind"], "title": data["title"],
              **current, "problems": problems,
              "scope": "local evidence only; not remote CI, authorization to publish, or proof of sandbox isolation"}
    write_json(directory / "gate.json", result)
    lines = [f"# Factory: {data['title']}", "", f"Kind: {data['kind']}",
             f"Candidate: `{fp}`", f"HEAD: `{current['head']}`", f"Ready: {result['ready']}", "",
             "## Acceptance criteria", "", *[f"- {k}: {v}" for k, v in data["criteria"].items()],
             "", "## Gate", "", *([f"- {p}" for p in problems] or ["- Required local evidence is current and passing."]),
             "", "Evidence: state.json and referenced JSON/log files in this run directory.",
             "Remote CI and PR head must be checked separately before claiming delivery."]
    (directory / "report.md").write_text("\n".join(lines) + "\n")
    emit(result)
    return 0 if result["ready"] else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    p = sub.add_parser("init")
    p.add_argument("--repo", required=True)
    p.add_argument("--kind", choices=KINDS, required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--criteria", required=True)
    p.add_argument("--base", default="HEAD")
    p.add_argument("--checks")
    p.add_argument("--max-rounds", type=positive, default=3)
    p.add_argument("--minutes", type=positive, default=60)
    p.set_defaults(func=cmd_init)
    for name, func in [("plan", cmd_plan), ("review", cmd_review), ("adjudicate", cmd_adjudicate), ("deliverable", cmd_deliverable)]:
        p = sub.add_parser(name)
        p.add_argument("--run", required=True)
        p.add_argument("--file", required=True)
        p.set_defaults(func=func)
    for name, func in [("begin", cmd_begin), ("tamper", cmd_tamper), ("gate", cmd_gate)]:
        p = sub.add_parser(name)
        p.add_argument("--run", required=True)
        p.set_defaults(func=func)
    p = sub.add_parser("snapshot")
    p.add_argument("--repo", required=True)
    p.set_defaults(func=lambda a: emit(snapshot(root(a.repo))))
    p = sub.add_parser("status")
    p.add_argument("--run", required=True)
    p.set_defaults(func=lambda a: emit(load(a.run)[1]))
    p = sub.add_parser("check")
    p.add_argument("--run", required=True)
    p.add_argument("--name", required=True, choices=["test", "build", "lint", "type", "ui", "integration"])
    p.add_argument("--cwd", default=".")
    p.add_argument("--timeout", type=positive, default=600)
    p.add_argument("argv", nargs=argparse.REMAINDER)
    p.set_defaults(func=cmd_check)
    p = sub.add_parser("repro")
    p.add_argument("--run", required=True)
    p.add_argument("--manifest", required=True)
    p.add_argument("--timeout", type=positive, default=300)
    p.set_defaults(func=cmd_repro)
    p = sub.add_parser("block")
    p.add_argument("--run", required=True)
    p.add_argument("--category", required=True, choices=["missing_access", "ambiguity", "scope_explosion", "impossible", "quota", "budget_exhausted", "infra", "dependency", "user_paused", "tamper", "review_unavailable"])
    p.add_argument("--reason", required=True)
    p.add_argument("--question", default="")
    p.add_argument("--resume-condition", required=True)
    p.set_defaults(func=cmd_block)
    p = sub.add_parser("resume")
    p.add_argument("--run", required=True)
    p.add_argument("--answer", required=True)
    p.add_argument("--extra-rounds", type=positive)
    p.add_argument("--extend-minutes", type=positive)
    p.add_argument("--authorization")
    p.set_defaults(func=cmd_resume)
    a = parser.parse_args()
    try:
        return a.func(a) or 0
    except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        emit({"error": str(exc), "status": "unavailable"})
        return 2


if __name__ == "__main__":
    sys.exit(main())
