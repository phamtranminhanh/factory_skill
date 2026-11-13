# Local dashboard

The suite includes a lightweight HTML dashboard adapted from the author's Margince Factory dashboard. It reads the Factory evidence ledger; it does not import Margince's board schema, four-reviewer requirement, automatic merges, or Claude profiles. The adaptation does not require the Margince application.

## Start and use

Resolve the helper path relative to this installed skill:

```sh
python3 /absolute/path/to/factory/scripts/factory_dashboard.py serve --port 8421
```

Open `http://127.0.0.1:8421`. It listens only on this computer. The server must remain running for the page to refresh; starting it does not start an agent worker. Do not start duplicate servers or stop unrelated processes if the port is occupied. Use another port and report the actual URL.

New evidence runs register automatically when `factory_run.py` saves state, even with the dashboard closed. Pointers live in `$CODEX_HOME/factory-dashboard/runs`, defaulting to `~/.codex/factory-dashboard/runs`; source and evidence stay in their original repositories. Tests can isolate this with `FACTORY_DASHBOARD_HOME`. Only registered runs appear; the server does not scan the user's disk.

To include an older run explicitly:

```sh
python3 /absolute/path/to/factory/scripts/factory_dashboard.py register /absolute/repo/.git/factory-runs/RUN_ID
```

The UI provides task filtering, board/list views, acceptance criteria, checks, review results, blockers, event history and plain-text evidence files. Demo mode is clearly separated and never writes real task state. The task composer copies a skill command for the user to send in Codex; it does not submit work or claim an agent has started.

## Truthfulness and boundaries

Stages reflect the most recently recorded workflow state, not a live agent heartbeat. A `working` run can be from an interrupted session. Show its last update; don't claim the server keeps it running. `ready` means the local gate passed on the current source fingerprint; it does not mean merged, deployed, PR created or remote CI green. Source changes invalidate displayed proof. Missing/malformed evidence and inaccessible repositories are shown as errors or stale state, not success.

The dashboard is read-only: no execute, approve, merge, credentials or agent-control endpoints. Files are restricted to named run artifacts and rendered as text. Evidence can still contain project-private data; don't expose this server beyond loopback. Freshness checks read the current tracked/nonignored tree, so very large repositories can refresh more slowly.

When changing the dashboard, verify empty/demo/live boards, filters, command copying, detail artifacts, stale/error state, keyboard Escape/focus, and narrow layout. Use isolated registries/fixtures; don't add mock jobs to a real run. Keep the frontend dependency-free and preserve provenance.
