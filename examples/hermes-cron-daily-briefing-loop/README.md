# Hermes Cron Daily Briefing Loop

This example shows the safe promotion path for a read-only Hermes daily briefing loop.

## Stage 1 — spec

Start from `loop-spec.yaml`. It is manual by default. Do not schedule until validate/score/dry-run pass.

```bash
hermes-loop validate examples/hermes-cron-daily-briefing-loop/loop-spec.yaml
hermes-loop score examples/hermes-cron-daily-briefing-loop/loop-spec.yaml
hermes-loop dry-run examples/hermes-cron-daily-briefing-loop/loop-spec.yaml --out /tmp/hermes-cron-daily-briefing
```

## Stage 2 — manual real run

Run the briefing manually in Hermes with read-only file/search tools. The run must produce a receipt with:

- inputs summarized, not copied raw;
- source list;
- deterministic check that sources are present;
- stop reason;
- no private paths/secrets in public artifacts.

## Stage 3 — cron-ready plan

Use `activation-plan.md`. Only then create a Hermes cron job.

Example cron prompt shape:

```text
Use the loop spec at <path>. Produce a read-only daily briefing. Do not post publicly. Do not access secrets. Write report and audit-grade receipt to the configured output paths. Stop and report if sources are unavailable or verification fails.
```

## Disable

Pause/remove the Hermes cron job if verification fails twice, source access changes, privacy scan fails, or the owner asks to stop.
