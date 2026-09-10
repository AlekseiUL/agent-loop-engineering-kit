# Agent Loop Engineering Kit for Hermes

Portable single-file version. A loop is a repeatable process with trigger, state, tools, verification, stop conditions, human gates and receipt. Start manual and read-only. No external side effects without approval.

Promotion path: write `loop-spec.yaml`, run `validate`, `score`, `audit-report`, then `dry-run`. Automate only after the audit report is `ok`, a manual Hermes run has a receipt, and an activation plan names rollback/disable steps.
