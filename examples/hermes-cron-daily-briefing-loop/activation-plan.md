# Activation Plan — Hermes Cron Daily Briefing

## Identity

- Loop name: `hermes-cron-daily-briefing-loop`
- Owner: human owner
- Reviewer: human owner before first scheduled run
- Hermes profile: chosen by installer
- Lifecycle stage: `dry_run`
- Risk class: `L1`

## Activation target

- Surface: `cron`
- Trigger details: daily local 09:00 after manual proof
- Disable switch: pause/remove the Hermes cron job
- State path: `state/hermes-cron-daily-briefing.json`
- Receipt path: `receipts/hermes-cron-daily-briefing.latest.md`

## Boundaries

- Allowed tools/toolsets: read/search files, write report/receipt only
- Forbidden actions: deletion, secrets, public posting, production deploy, payments
- Allowed read paths: configured notes/source folder only
- Allowed write paths: configured reports/receipts/state folders only
- Network policy: no network unless source list explicitly requires public read-only URLs
- Data classification: private by default
- Secrets policy: never read or print secrets

## Verification

- `hermes-loop validate examples/hermes-cron-daily-briefing-loop/loop-spec.yaml`
- `hermes-loop score examples/hermes-cron-daily-briefing-loop/loop-spec.yaml`
- `hermes-loop dry-run examples/hermes-cron-daily-briefing-loop/loop-spec.yaml --out /tmp/hermes-cron-daily-briefing`
- `hermes-loop privacy-scan .`

## Operations

- Max iterations: 1
- Max runtime: 15 minutes
- Retry/backoff: no automatic retry in v0.1
- Idempotency: one receipt per date/run id
- Concurrency: do not run if previous briefing is still active
- Escalation: stop and report on missing sources, privacy finding or failed verification

## Rollback

- Pause/remove cron job.
- Keep last known good report/receipt.
- Delete only generated report/receipt files after explicit human approval.
