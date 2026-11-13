# Executable evidence and ledger

Run the helper with Python 3.10+; no third-party Python dependency is required. Resolve `factory/scripts/factory_run.py` from the installed skill directory, assign its absolute path to `factory_tool`, and keep `factory_run` as the absolute run path printed by `init`. Do not repurpose system environment variables. Quote shell paths; pass commands as argv after `--`, without `eval`.

## Initialize before edits

Create a temporary JSON array of criterion strings outside the target source tree, then:

```sh
python3 "$factory_tool" init --repo /absolute/task/worktree --kind bugfix --title "Fix empty cart total" --criteria /tmp/task-criteria.json --base HEAD --checks test --max-rounds 3 --minutes 60
```

For a review of existing changes, explicitly choose the merge base as `--base`; for a new implementation use the clean starting HEAD. The helper stores the resolved commit, not a moving branch name. In a repository with no commit yet, create a baseline only if authorized; otherwise explain the missing Git baseline.

Plan JSON:

```json
{"approach":"Change the empty-cart branch; preserve nonempty behavior.","criteria":["C1","C2"],"files":["cart.py","tests/test_cart.py"],"tests":{"C1":"test_empty","C2":"test_nonempty"},"out_of_scope":["tax changes"]}
```

```sh
python3 "$factory_tool" plan --run "$factory_run" --file /tmp/task-plan.json
python3 "$factory_tool" begin --run "$factory_run"
python3 "$factory_tool" snapshot --repo /absolute/task/worktree
```

`begin` is also required for every corrective implementation round. User-directed extension uses `resume` with an explicit authorization note; do not silently reset the run. Initial bounds may be chosen for the stated task size.

## Verification

Examples below are examples only; use the project's real commands:

```sh
python3 "$factory_tool" tamper --run "$factory_run"
python3 "$factory_tool" check --run "$factory_run" --name test --timeout 600 -- python3 -m pytest -q
python3 "$factory_tool" check --run "$factory_run" --name build --cwd web --timeout 600 -- npm run build
```

Exit codes: 0 passing recorded result, 1 an executed check/gate did not pass, 2 invalid input or unavailable machinery. Inspect the JSON and referenced log; do not treat all nonzero exits as product defects. Timeouts kill the launched process group. Log files retain at most the last 2 MiB after execution; commands still need sensible output bounds while running. Never put credentials in arguments or ask the test runner to print them.

The candidate fingerprint covers tracked and nonignored untracked files, deletion, executable bit and symlink target. HEAD is recorded separately so committing identical verified bytes does not invalidate proof. Ignored dependencies/configuration, external services, Git configuration and remote state are not part of this fingerprint; inspect and disclose their influence. Submodules require separate verification and are refused by this helper. Keep verification isolated from unrelated writers. A command that changes source makes its receipt stale.

A zero exit alone does not prove meaningful coverage. The verifier must check discovered tests, assertions and the actual import/build target. In particular, editable Python installations can point to another checkout. The helper sets PYTHONPATH to the tested checkout's `src` and root; project-specific loaders can still require extra inspection.

## Bugfix reproduction

Manifest, placed outside candidate source:

```json
{"files":["tests/test_cart.py"],"argv":["python3","-m","pytest","-q","tests/test_cart.py::test_empty"],"cwd":".","failure_pattern":"AssertionError|assert .* == .*","setup_argv":[]}
```

```sh
python3 "$factory_tool" repro --run "$factory_run" --manifest /tmp/task-repro.json --timeout 300
```

The helper creates a disposable worktree at the pinned baseline, optionally runs explicit setup argv there, copies only named test/test-support files from the candidate, and runs the same test command before/after. It removes only the worktree it created. Use a narrow regression test and a specific expected behavioral failure pattern. Missing modules, syntax/collection errors, no tests collected and timeouts do not establish a reproduction. Setup that changes nonignored source is refused. No product source may be copied into the baseline. Inspect copied fixtures/conftest for behavior spoofing. For ecosystems requiring builds, provide the project-specific setup command; do not silently skip the baseline run when the environment is missing.

Repro is mandatory for a completed bugfix workflow. If it cannot run, deliver the partial change with a blocker and the missing evidence, not a verified-success claim. An explicit user waiver can be reported as a waiver; the helper's bugfix gate deliberately remains incomplete.

## Tamper adjudication

The detector is vendored unchanged from no_human and handles known Python/JS/TS/Java test patterns. It is heuristic, not exhaustive; new test styles, balanced deletions/additions and generated fixtures need independent review. The wrapper uses NUL-separated Git paths, including Unicode names. The upstream license and provenance live beside the vendored file.

If flagged, give all reasons to the independent reviewer. Legitimate changes must be demanded by a named acceptance criterion, with a replacement check where appropriate. Record:

```json
{"fingerprint":"COPY_CURRENT_FINGERPRINT","reviewer_id":"ACTUAL_SESSION_ID","independent":true,"verdict":"legitimate","decisions":[{"reason":"COPY_EXACT_FLAGGED_REASON","criterion":"C1","evidence":"The approved requirement removes X; test_y checks the replacement behavior."}]}
```

Use `adjudicate --run ... --file ...`. `tampering` requires repair; `cannot_decide` requires clarification or more evidence. A repeated unexplained test-weakening attempt should stop, not consume unlimited rounds.

## Independent review

Record a snapshot before giving the candidate to the reviewer. Have the reviewer return:

```json
{"fingerprint":"COPY_CURRENT_FINGERPRINT","reviewer_id":"ACTUAL_SESSION_ID","independent":true,"verdict":"pass","goal_reachable":true,"criteria":[{"id":"C1","status":"met","evidence":"tests/test_cart.py:12 exercises the public entry point; check log …"}],"findings":[],"reviewed_paths":["cart.py","tests/test_cart.py"],"limitations":[]}
```

Each criterion appears exactly once. Status is `met`, `not_met` or `unknown`. Findings have `severity` (`critical`, `high`, `medium`, `low`, `nit`), `file`/`line` or an evidence `artifact`, and `evidence` explaining concrete impact. Blocking findings cannot be cleared by an overall PASS. Invalid citations are refused, not silently treated as passed. File/line existence is not proof of the finding's truth; the reviewer must establish that. Material incomplete review coverage is an unknown criterion / FAIL, not merely a note under a PASS.

```sh
python3 "$factory_tool" review --run "$factory_run" --file /tmp/task-review.json
python3 "$factory_tool" gate --run "$factory_run"
```

The helper cannot authenticate `reviewer_id` or `independent`; the coordinator must use an actual distinct session. It also cannot prevent an agent with local file access from editing the ledger. Evidence is an auditable workflow, not a tamper-proof security boundary. Keep reviewer output and tool receipts available for inspection.

For report-only kinds, write the report outside source, run `deliverable --run ... --file ...`, and supply its returned `sha256` as `deliverable_sha256` in the review. The gate requires both the exact reviewed report and an unchanged repository. Present the report contents to the user; a ledger path alone is not the deliverable.

`gate` writes `gate.json` and `report.md`. A source/report change invalidates corresponding proofs. The summary is local evidence; remote checks and PR identity are handled separately.

## Block and resume

```sh
python3 "$factory_tool" block --run "$factory_run" --category missing_access --reason "CI logs are inaccessible" --question "Which connected account can read this run?" --resume-condition "The failed run's logs are readable"
python3 "$factory_tool" status --run "$factory_run"
python3 "$factory_tool" resume --run "$factory_run" --answer "User supplied the CI log artifact"
```

Resume resolves the recorded blocker; it does not reset attempts/deadlines or prove that credentials now work. Confirm the new evidence, then begin the next bounded round. Read the specific command help for explicitly authorized budget extensions.
