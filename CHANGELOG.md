# Changelog

## 0.1.1 - 2026-06-23

### Added

- `hermes-loop audit-report` for a CI-friendly loop promotion gate with JSON and Markdown output.
- Production readiness checklist under `docs/09-production-readiness.md`.
- Source-tree `scripts/audit_report.py` entrypoint.

### Changed

- Replaced duplicated source-tree CLI scripts with thin wrappers around the installable `hermes_loop` package modules.
- Completed MIT license text so GitHub/package consumers can identify the license reliably.

## 0.1.0

Public v0.1 contract for the Hermes Agent Loop Kit.

### Added

- Installable `hermes-loop` CLI with `init`, `validate`, `score`, `dry-run`, `render-receipt`, `privacy-scan` and `smoke` commands.
- Loop spec schema contract `schema_version: "1.0"`.
- Audit-grade run-record and receipt contract v1.
- Safety-first validator, usefulness scorer, privacy scanner and dry-run receipt generator.
- Hermes activation plan template and lifecycle guide.
- Threat model for Hermes loops.
- Hermes cron daily briefing example.
- Installed CLI smoke script for release checks.

### Boundaries

- v0.1 designs, validates, dry-runs and audits loop contracts.
- v0.1 does not execute real agent tasks, activate Hermes cron/webhook/Kanban jobs, or replace Hermes runtime/scheduler.
- Breaking changes to loop spec schema or receipt shape are reserved for v0.2+.
