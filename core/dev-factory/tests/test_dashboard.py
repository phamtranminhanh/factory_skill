"""Exercise real ledger projection and HTTP boundaries using isolated runs."""
import json
from pathlib import Path
import sys
import threading
from http.server import ThreadingHTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError

from test_factory_run import EvidenceTests, TOOL

sys.path.insert(0, str(TOOL.parent))
from factory_dashboard import Store, handler_for
from dashboard_store import register


class DashboardTests(EvidenceTests):
    # Only dashboard tests are inherited by discovery through this class below.
    def setup_store(self):
        self.init("bugfix")
        self.store = Store(self.home / "dashboard")
        self.identity = register(self.runpath, self.home / "dashboard")

    def test_dashboard_registers_run_without_server(self):
        self.setup_store()
        board = self.store.board()
        self.assertEqual(len(board["jobs"]), 1)
        job = board["jobs"][0]
        self.assertEqual(job["id"], self.identity)
        self.assertFalse(job["ready"])
        self.assertEqual(job["checks"][0]["status"], "not_run")
        self.assertIn("round_started", [x["event"] for x in job["events"]])

    def test_dashboard_ready_invalidates_after_uncommitted_edit(self):
        self.setup_store(); self.fix(); self.run_checks(); self.repro()
        self.call("tamper", "--run", self.runpath); self.record_review()
        self.call("gate", "--run", self.runpath)
        self.assertTrue(self.store.board()["jobs"][0]["ready"])
        (self.repo / "calc.py").write_text("def add(a,b): return -999\n")
        job = self.store.board()["jobs"][0]
        self.assertFalse(job["ready"])
        self.assertTrue(job["stale"])
        self.assertEqual(job["checks"][0]["status"], "stale")

    def test_dashboard_blocked_and_corrupt_runs_do_not_fake_success(self):
        self.setup_store()
        self.call("block", "--run", self.runpath, "--category", "missing_access", "--reason", "Need logs", "--resume-condition", "Logs available")
        job = self.store.board()["jobs"][0]
        self.assertEqual(job["stage"], "blocked")
        self.assertEqual(job["blocker"]["reason"], "Need logs")
        (Path(self.runpath) / "state.json").write_text("{")
        board = self.store.board()
        self.assertEqual(board["jobs"], [])
        self.assertEqual(len(board["errors"]), 1)

    def test_dashboard_artifacts_allowlist_and_symlink(self):
        self.setup_store()
        self.assertEqual(json.loads(self.store.artifact(self.identity, "state.json"))["kind"], "bugfix")
        private = Path(self.runpath) / "unrelated.txt"; private.write_text("private")
        for name in ["../state.json", str(private), "unrelated.txt"]:
            with self.assertRaises(ValueError):
                self.store.artifact(self.identity, name)
        target = Path(self.runpath) / "events.jsonl"
        target.unlink(); target.symlink_to(private)
        with self.assertRaises(ValueError):
            self.store.artifact(self.identity, "events.jsonl")

    def test_dashboard_report_review_tracks_deliverable_before_gate(self):
        self.init("investigation")
        self.store = Store(self.home / "dashboard")
        self.identity = register(self.runpath, self.home / "dashboard")
        output = self.home / "report.txt"; output.write_text("Report A")
        receipt = self.call("deliverable", "--run", self.runpath, "--file", output)
        review = self.review(deliverable_sha256=receipt["sha256"])
        self.call("review", "--run", self.runpath, "--file", review)
        self.assertEqual(self.store.describe(self.identity)["review"]["status"], "pass")
        output.write_text("Report B")
        self.call("deliverable", "--run", self.runpath, "--file", output)
        job = self.store.describe(self.identity)
        self.assertEqual(job["review"]["status"], "stale")
        self.assertTrue(job["stale"])

    def test_dashboard_http_rejects_foreign_origin_host_and_write(self):
        self.setup_store()
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler_for(self.store))
        thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
        base = f"http://127.0.0.1:{server.server_port}"
        try:
            with urlopen(base + "/api/board") as response:
                self.assertEqual(len(json.load(response)["jobs"]), 1)
                self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
            for headers in [{"Origin": "https://example.invalid"}, {"Host": "attacker.invalid"}, {"Origin": "null"}]:
                with self.assertRaises(HTTPError) as error:
                    urlopen(Request(base + "/api/board", headers=headers))
                self.assertEqual(error.exception.code, 403)
                error.exception.close()
            with self.assertRaises(HTTPError) as error:
                urlopen(Request(base + "/api/board", data=b"{}", method="POST"))
            self.assertEqual(error.exception.code, 501)
            error.exception.close()
            with self.assertRaises(HTTPError) as error:
                urlopen(base + "/api/artifact?run=" + self.identity + "&file=..%2Fstate.json")
            self.assertEqual(error.exception.code, 400)
            error.exception.close()
        finally:
            server.shutdown(); server.server_close(); thread.join()


# Reuse fixture helpers without re-running the parent's unrelated test methods.
for name in tuple(vars(EvidenceTests)):
    if name.startswith("test_"):
        setattr(DashboardTests, name, None)

def load_tests(loader, suite, pattern):
    return loader.loadTestsFromTestCase(DashboardTests)
