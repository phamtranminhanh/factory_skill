#!/usr/bin/env python3
"""Read-only, loopback-only dashboard for registered Factory evidence runs."""
from __future__ import annotations

import argparse
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import sys
import time
from urllib.parse import parse_qs, urlsplit

from dashboard_store import register, registry_root, run_id
from factory_run import snapshot, root, REPORT_ONLY

MAX_ARTIFACT = 2 * 1024 * 1024
MAX_JSON = 4 * 1024 * 1024
IDENTITY = re.compile(r"^[0-9a-f]{24}$")
FILENAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,180}$")
UI = Path(__file__).resolve().parents[1] / "dashboard" / "index.html"


def read_json(path):
    with Path(path).open("rb") as source:
        data = source.read(MAX_JSON + 1)
    if len(data) > MAX_JSON:
        raise ValueError("JSON record is too large")
    return json.loads(data)


def safe_file(directory, name):
    if not isinstance(name, str) or not FILENAME.fullmatch(name):
        raise ValueError("Invalid artifact name")
    path = directory / name
    if path.is_symlink() or path.resolve().parent != directory.resolve():
        raise ValueError("Artifact must stay inside its run")
    return path


class Store:
    def __init__(self, registry=None):
        self.registry = Path(registry) if registry is not None else registry_root()

    def directory(self, identity):
        if not IDENTITY.fullmatch(identity):
            raise ValueError("Invalid run ID")
        pointer = self.registry / "runs" / (identity + ".json")
        if pointer.is_symlink():
            raise ValueError("Invalid registry pointer")
        directory = Path(read_json(pointer)["run"]).resolve()
        if run_id(directory) != identity:
            raise ValueError("Mismatched registry pointer")
        return directory

    def describe(self, identity):
        directory = self.directory(identity)
        state = read_json(safe_file(directory, "state.json"))
        if state.get("schema") != 1:
            raise ValueError("Unsupported run schema")
        files = {"state.json": "Trạng thái", "events.jsonl": "Lịch sử"}
        for name, label in (("gate.json", "Kết quả tổng hợp"), ("report.md", "Báo cáo")):
            if safe_file(directory, name).is_file():
                files[name] = label

        def evidence(name, label):
            if not name:
                return None
            value = read_json(safe_file(directory, name))
            if not isinstance(value, dict):
                raise ValueError("Invalid evidence record")
            files[name] = label
            for row in (value, value.get("before"), value.get("after")):
                if isinstance(row, dict) and row.get("log"):
                    log = row["log"]
                    if safe_file(directory, log).is_file():
                        files[log] = "Log · " + label
            return value

        # Do not use HEAD alone: uncommitted edits also invalidate evidence.
        current, error = None, None
        try:
            current = snapshot(root(state["repo"]))["fingerprint"]
        except Exception as exc:
            error = "Không kiểm tra được phiên bản hiện tại: " + str(exc)

        def fresh(value):
            if value and (current is None or value.get("fingerprint") != current):
                value = dict(value, status="stale")
            return value

        checks = []
        for name in dict.fromkeys([*state.get("required_checks", []), *state.get("checks", {})]):
            value = fresh(evidence(state.get("checks", {}).get(name), "Kiểm tra · " + name))
            checks.append(dict(value or {"status": "not_run"}, name=name))
        reviews = [fresh(evidence(name, "Review · " + str(i + 1))) for i, name in enumerate(state.get("reviews", []))]
        review = reviews[-1] if reviews else None
        tamper = fresh(evidence(state.get("tamper"), "Kiểm tra thay đổi test"))
        repro = fresh(evidence(state.get("repro"), "Tái hiện lỗi"))
        evidence(state.get("adjudication"), "Giải trình thay đổi test")
        evidence(state.get("plan"), "Kế hoạch")
        deliverable = state.get("deliverable")
        deliverable_changed = False
        if deliverable:
            name = deliverable["file"]
            if safe_file(directory, name).is_file():
                files[name] = "Kết quả bàn giao"
            if state.get("kind") in REPORT_ONLY:
                deliverable_changed = (not safe_file(directory, name).is_file()
                    or hashlib.sha256(safe_file(directory, name).read_bytes()).hexdigest() != deliverable["sha256"])
        if review and state.get("kind") in REPORT_ONLY and (deliverable_changed or not deliverable
                or review.get("deliverable_sha256") != deliverable["sha256"]):
            review = dict(review, status="stale")
        gate = read_json(safe_file(directory, "gate.json")) if "gate.json" in files else None
        stale = bool(gate and (current is None or gate.get("fingerprint") != current
                     or safe_file(directory, "gate.json").stat().st_mtime < state.get("updated_at", 0)))
        stale = stale or deliverable_changed
        ready = bool(gate and gate.get("ready") is True and not stale and state.get("phase") != "blocked")
        phase = state.get("phase", "intake")
        if phase == "blocked":
            stage = "blocked"
        elif ready:
            stage = "ready"
        elif phase == "intake":
            stage = "planning" if state.get("plan") else "intake"
        elif phase == "planned":
            stage = "planning"
        elif review or any(c["status"] == "pass" for c in checks):
            stage = "review"
        else:
            stage = "working"
        events = []
        eventpath = safe_file(directory, "events.jsonl")
        if eventpath.exists():
            with eventpath.open("rb") as source:
                source.seek(0, 2)
                total = source.tell()
                source.seek(max(0, total - MAX_ARTIFACT))
                lines = source.read().decode("utf-8", errors="replace").splitlines()
            for line in lines[-100:]:
                try:
                    item = json.loads(line)
                    if isinstance(item, dict):
                        events.append(item)
                except ValueError:
                    continue  # An in-flight append must not break the board.
        return {"id": identity, "title": state["title"], "kind": state["kind"], "repo": state["repo"],
                "stage": stage, "phase": phase, "round": state["round"], "max_rounds": state["max_rounds"],
                "updated_at": state.get("updated_at", 0), "created_at": state.get("created_at", 0),
                "criteria": state["criteria"], "checks": checks, "review": review, "tamper": tamper,
                "repro": repro, "blocker": state.get("blocker") if phase == "blocked" else None,
                "ready": ready, "stale": stale or any(x and x.get("status") == "stale" for x in [review, tamper, repro, *checks]),
                "files": [{"name": name, "label": label} for name, label in files.items()],
                "events": events, "error": error}

    def board(self):
        jobs, errors = [], []
        for pointer in sorted((self.registry / "runs").glob("*.json")):
            try:
                jobs.append(self.describe(pointer.stem))
            except Exception as exc:
                errors.append({"id": pointer.stem, "message": str(exc)})
        jobs.sort(key=lambda job: job["updated_at"], reverse=True)
        return {"version": 1, "jobs": jobs, "errors": errors, "generated_at": time.time()}

    def artifact(self, identity, name):
        job = self.describe(identity)
        if name not in {item["name"] for item in job["files"]}:
            raise ValueError("Artifact is not referenced by this run")
        path = safe_file(self.directory(identity), name)
        with path.open("rb") as source:
            data = source.read(MAX_ARTIFACT + 1)
        suffix = "\n[Đã giới hạn nội dung ở 2 MiB]" if len(data) > MAX_ARTIFACT else ""
        return data[:MAX_ARTIFACT].decode("utf-8", errors="replace") + suffix


def handler_for(store):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass

        def send(self, code, data, content_type="application/json; charset=utf-8"):
            body = data if isinstance(data, bytes) else data.encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            port = self.server.server_port
            hosts = {f"127.0.0.1:{port}", f"localhost:{port}"}
            origin = self.headers.get("Origin")
            if self.headers.get("Host") not in hosts or (origin and origin not in {"http://" + host for host in hosts}):
                self.send(403, '{"error":"Local requests only"}')
                return
            url = urlsplit(self.path)
            try:
                if url.path in ("/", "/index.html"):
                    self.send(200, UI.read_bytes(), "text/html; charset=utf-8")
                elif url.path == "/api/board":
                    self.send(200, json.dumps(store.board(), ensure_ascii=False))
                elif url.path == "/api/artifact":
                    query = parse_qs(url.query, strict_parsing=True)
                    if set(query) != {"run", "file"} or any(len(value) != 1 for value in query.values()):
                        raise ValueError("Expected one run and one file")
                    self.send(200, store.artifact(query["run"][0], query["file"][0]), "text/plain; charset=utf-8")
                else:
                    self.send(404, '{"error":"Not found"}')
            except (ValueError, KeyError, TypeError):
                self.send(400, '{"error":"Invalid or unavailable run artifact"}')
            except OSError:
                self.send(404, '{"error":"File unavailable"}')

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("register", help="Include an existing run in the local dashboard")
    p.add_argument("run", type=Path)
    p = sub.add_parser("serve", help="Serve the read-only dashboard; does not start agents")
    p.add_argument("--port", type=int, default=8421)
    args = parser.parse_args()
    if args.command == "register":
        print(json.dumps({"id": register(args.run)}))
        return
    if not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    if not UI.is_file():
        parser.error("Dashboard UI is missing; reinstall the complete Factory skill")
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler_for(Store()))
    print(f"Factory dashboard: http://127.0.0.1:{args.port} — read-only, no agent worker", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
