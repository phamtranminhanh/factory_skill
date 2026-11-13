"""Behavioral tests of evidence freshness, proof gates and bounded execution."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

TOOL = Path(__file__).resolve().parents[1] / "factory/scripts/factory_run.py"


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="factory-tests-")
        self.home = Path(self.temp.name)
        self.env = dict(os.environ, FACTORY_DASHBOARD_HOME=str(self.home / "dashboard"))
        self.repo = self.home / "repo"
        self.repo.mkdir()
        (self.repo / "calc.py").write_text("def add(a, b):\n    return a - b\n")
        (self.repo / "tests").mkdir()
        (self.repo / "tests/test_existing.py").write_text(
            "import unittest\nfrom calc import add\nclass Existing(unittest.TestCase):\n"
            "    def test_zero(self):\n        self.assertEqual(add(1, 0), 1)\n")
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Factory Tests")
        self.git("config", "user.email", "factory-tests@example.invalid")
        self.git("add", ".")
        self.git("commit", "-m", "baseline")
        self.runpath = None

    def tearDown(self):
        self.temp.cleanup()

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args], stderr=subprocess.PIPE).decode().strip()

    def write(self, name, value):
        p = self.home / name
        p.write_text(json.dumps(value))
        return str(p)

    def call(self, *args, code=0, env=None):
        result = subprocess.run([sys.executable, str(TOOL), *map(str, args)], capture_output=True, text=True, env=dict(self.env, **(env or {})))
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def init(self, kind="feature", rounds=3):
        criteria = self.write("criteria.json", ["Addition returns a plus b"])
        result = self.call("init", "--repo", self.repo, "--kind", kind, "--title", "Add correctly", "--criteria", criteria, "--max-rounds", rounds)
        self.runpath = result["run"]
        plan = self.write("plan.json", {"approach": "Fix arithmetic and test public function", "criteria": ["C1"]})
        self.call("plan", "--run", self.runpath, "--file", plan)
        self.call("begin", "--run", self.runpath)

    def fix(self, vacuous=False):
        (self.repo / "calc.py").write_text("def add(a, b):\n    return a + b\n")
        assertion = "self.assertTrue(True)" if vacuous else "self.assertEqual(add(1, 2), 3)"
        (self.repo / "tests/test_repro.py").write_text(
            "import unittest\nfrom calc import add\nclass Repro(unittest.TestCase):\n"
            "    def test_add(self):\n        " + assertion + "\n")

    def run_checks(self):
        return self.call("check", "--run", self.runpath, "--name", "test", "--", sys.executable,
                         "-m", "unittest", "discover", "-s", "tests", "-v")

    def review(self, **changes):
        fingerprint = self.call("snapshot", "--repo", self.repo)["fingerprint"]
        report = {"fingerprint": fingerprint, "reviewer_id": "independent-test-session", "independent": True,
                  "verdict": "pass", "goal_reachable": True,
                  "criteria": [{"id": "C1", "status": "met", "evidence": "calc.py:2 and executed regression"}], "findings": []}
        report.update(changes)
        return self.write("review.json", report)

    def record_review(self):
        return self.call("review", "--run", self.runpath, "--file", self.review())

    def repro(self, command=None, code=0):
        manifest = {"files": ["tests/test_repro.py"], "argv": command or [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_repro.py", "-v"],
                    "failure_pattern": "AssertionError", "cwd": "."}
        return self.call("repro", "--run", self.runpath, "--manifest", self.write("repro.json", manifest), code=code)

    def test_full_bugfix_requires_real_red_green_and_preserves_base(self):
        self.init("bugfix")
        baseline = self.git("rev-parse", "HEAD")
        self.fix()
        self.run_checks()
        self.call("tamper", "--run", self.runpath)
        proof = self.repro()
        self.assertEqual(proof["before"]["exit_code"], 1)
        self.assertEqual(proof["after"]["exit_code"], 0)
        self.record_review()
        self.assertTrue(self.call("gate", "--run", self.runpath)["ready"])
        self.assertEqual(self.git("rev-parse", "HEAD"), baseline)
        self.assertEqual(len(self.git("worktree", "list", "--porcelain").split("worktree ")) - 1, 1)

    def test_missing_proof_is_not_a_verified_bugfix(self):
        self.init("bugfix")
        self.fix(); self.run_checks(); self.call("tamper", "--run", self.runpath); self.record_review()
        self.assertIn("reproduction: NOT RUN", self.call("gate", "--run", self.runpath, code=1)["problems"])

    def test_repro_works_with_symlinked_temporary_directory(self):
        self.init("bugfix"); self.fix()
        actual = self.home / "actual-temp"; actual.mkdir()
        alias = self.home / "temp-alias"; alias.symlink_to(actual, target_is_directory=True)
        manifest = {"files": ["tests/test_repro.py"], "argv": [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], "failure_pattern": "AssertionError"}
        env = {"TMPDIR": str(alias)}
        proof = self.call("repro", "--run", self.runpath, "--manifest", self.write("repro.json", manifest), env=env)
        self.assertEqual(proof["status"], "pass")
        self.assertEqual(list(actual.iterdir()), [])

    def test_repro_setup_obeys_shared_deadline(self):
        self.init("bugfix"); self.fix()
        statepath = Path(self.runpath) / "state.json"
        state = json.loads(statepath.read_text()); state["deadline"] = time.time() + 0.8
        statepath.write_text(json.dumps(state))
        manifest = {"files": ["tests/test_repro.py"], "argv": [sys.executable, "-m", "unittest"],
                    "failure_pattern": "AssertionError", "setup_argv": [[sys.executable, "-c", "import time; time.sleep(10)"]]}
        started = time.monotonic()
        proof = self.call("repro", "--run", self.runpath, "--timeout", 20, "--manifest", self.write("repro.json", manifest), code=1)
        self.assertLess(time.monotonic() - started, 5)
        self.assertEqual(proof["status"], "error")

    def test_vacuous_regression_is_refused(self):
        self.init("bugfix"); self.fix(vacuous=True)
        proof = self.repro(code=1)
        self.assertEqual(proof["before"]["exit_code"], 0)
        self.assertEqual(proof["status"], "fail")

    def test_import_error_is_not_behavioral_failure(self):
        self.init("bugfix"); self.fix()
        (self.repo / "tests/test_repro.py").write_text("import module_that_does_not_exist\n")
        proof = self.repro(code=1)
        self.assertEqual(proof["status"], "error")

    def test_source_change_invalidates_prior_passes(self):
        self.init(); self.fix(); self.run_checks(); self.call("tamper", "--run", self.runpath); self.record_review()
        (self.repo / "calc.py").write_text("def add(a, b):\n    return 0\n")
        gate = self.call("gate", "--run", self.runpath, code=1)
        self.assertTrue(any("stale" in x for x in gate["problems"]))

    def test_commit_of_identical_bytes_preserves_evidence(self):
        self.init(); self.fix(); self.run_checks(); self.call("tamper", "--run", self.runpath); self.record_review()
        old = self.call("snapshot", "--repo", self.repo)
        self.git("add", "."); self.git("commit", "-m", "fix")
        gate = self.call("gate", "--run", self.runpath)
        self.assertEqual(gate["fingerprint"], old["fingerprint"])
        self.assertNotEqual(gate["head"], old["head"])

    def test_blocking_finding_overrides_claimed_pass(self):
        self.init()
        path = self.review(findings=[{"severity": "high", "file": "calc.py", "line": 2, "evidence": "subtracts instead of adding"}])
        report = self.call("review", "--run", self.runpath, "--file", path, code=1)
        self.assertEqual(report["status"], "fail")

    def test_invalid_citation_never_becomes_pass(self):
        self.init()
        path = self.review(findings=[{"severity": "high", "file": "calc.py", "line": 999, "evidence": "claimed issue"}])
        self.call("review", "--run", self.runpath, "--file", path, code=2)

    def test_review_of_changed_candidate_is_refused(self):
        self.init()
        report = self.review()
        (self.repo / "calc.py").write_text("x = 1\n")
        self.call("review", "--run", self.runpath, "--file", report, code=2)

    def test_unicode_test_deletion_is_detected(self):
        self.git("mv", "tests/test_existing.py", "tests/test_đúng.py")
        self.git("commit", "-m", "Unicode test")
        self.init()
        (self.repo / "tests/test_đúng.py").unlink()
        result = self.call("tamper", "--run", self.runpath, code=1)
        self.assertTrue(result["tampered"])

    def test_failed_command_is_not_pass(self):
        self.init()
        result = self.call("check", "--run", self.runpath, "--name", "test", "--", sys.executable, "-c", "raise SystemExit(5)", code=1)
        self.assertEqual(result["exit_code"], 5)

    def test_round_budget_survives_resume(self):
        self.init(rounds=1)
        self.call("block", "--run", self.runpath, "--category", "ambiguity", "--reason", "Need input", "--resume-condition", "User answers")
        self.call("resume", "--run", self.runpath, "--answer", "Answer received")
        self.call("begin", "--run", self.runpath, code=2)
        self.call("block", "--run", self.runpath, "--category", "budget_exhausted", "--reason", "No rounds left", "--resume-condition", "Explicit budget increase")
        self.call("resume", "--run", self.runpath, "--answer", "Continue", "--extra-rounds", 1, code=2)

    def test_report_only_requires_same_report_and_unchanged_repo(self):
        self.init("investigation")
        output = self.home / "report.txt"; output.write_text("add subtracts at calc.py:2")
        d = self.call("deliverable", "--run", self.runpath, "--file", output)
        review = self.review(deliverable_sha256=d["sha256"])
        self.call("review", "--run", self.runpath, "--file", review)
        self.assertTrue(self.call("gate", "--run", self.runpath)["ready"])
        output.write_text("different conclusion")
        self.call("deliverable", "--run", self.runpath, "--file", output)
        self.assertFalse(self.call("gate", "--run", self.runpath, code=1)["ready"])

    def test_timeout_kills_spawned_process_group(self):
        self.init()
        marker = self.home / "child-survived"
        child = f"import time; from pathlib import Path; time.sleep(2); Path({str(marker)!r}).write_text('bad')"
        parent = f"import subprocess,sys,time; subprocess.Popen([sys.executable,'-c',{child!r}]); time.sleep(10)"
        result = self.call("check", "--run", self.runpath, "--name", "test", "--timeout", 1, "--", sys.executable, "-c", parent, code=1)
        self.assertTrue(result["timed_out"])
        time.sleep(1.5)
        self.assertFalse(marker.exists())

    def test_source_mutating_check_is_stale(self):
        self.init()
        result = self.call("check", "--run", self.runpath, "--name", "test", "--", sys.executable, "-c", "from pathlib import Path; Path('calc.py').write_text('changed')", code=1)
        self.assertEqual(result["status"], "stale")


if __name__ == "__main__":
    unittest.main()
