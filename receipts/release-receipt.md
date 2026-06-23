# Release Receipt

## Product

Agent Loop Engineering Kit

## Release

- Version: `0.1.1`
- Status: `product-readiness polish`
- Repository: <https://github.com/AlekseiUL/agent-loop-engineering-kit>
- Commit: this receipt is committed with `feat: add loop promotion audit gate`; use `git rev-parse HEAD` for the immutable SHA after checkout/tagging.

## Release contract

`v0.1.1` is a design, validation, promotion-audit, dry-run, receipt and privacy-scan kit for Hermes Agent loop contracts.

It is not a Hermes runtime, scheduler, cron manager, webhook runner, or proof that model output is true.

## What changed since 0.1.0

- Added `hermes-loop audit-report` for a CI-friendly loop promotion gate with JSON and Markdown output.
- Added `scripts/audit_report.py` source-tree entrypoint.
- Added `docs/09-production-readiness.md` with production readiness and activation gates.
- Replaced duplicated source-tree CLI scripts with thin wrappers around installable package modules.
- Completed the MIT license text and switched project metadata to SPDX-style `license = "MIT"`.
- Made resource directories explicit packages to remove build warnings.
- Bumped package version to `0.1.1`.

## Included surfaces

- README with English and Russian product explanation.
- `START-HERE.md` first-user path.
- Hermes-first docs and lifecycle guide.
- Threat model and production-readiness checklist.
- Loop spec JSON schema with `schema_version: "1.0"`.
- Run-record and receipt schema contract v1.
- Templates: loop spec, activation plan, verification contract, human gate policy, receipt.
- Examples including deliberately unsafe examples that must fail validation/audit.
- Installable `hermes-loop` CLI.
- Source-tree script wrappers under `scripts/`.
- Pytest regression suite.
- GitHub Actions smoke workflow.
- Portable single-file kit under `kit/`.

## Verification run

Executed locally from repository checkout on 2026-06-23.

```bash
pytest -q
bash scripts/smoke.sh
bash scripts/installed_cli_smoke.sh
hermes-loop privacy-scan .
python -m build
pip install dist/agent_loop_engineering_kit-0.1.1-py3-none-any.whl
hermes-loop audit-report <loop-spec> --json
hermes-loop dry-run <loop-spec> --out <dir> --json
```

## Result

- Tests: `27 passed`.
- Repository smoke: PASS.
- Installed CLI smoke: PASS.
- Privacy scan: PASS.
- Package build: PASS, produced sdist and wheel.
- Wheel install smoke: PASS.
- Good loop audit: `ok: true`, `ready_for: manual_read_only_run`.
- Bad L3 cron repo editor audit: blocked as expected.
- Bad L3 cron repo editor validation: blocked as expected.
- Receipt rendering: PASS.

## Safety position

- No always-on cron by default.
- No auto-push from loop specs.
- No auto-merge.
- No deploy.
- No public posting.
- No secret access.
- No writes to Hermes memory, skills, cron, plugins, config or auth by default.
- Cross-profile access requires explicit approval.
- L3 coding loops require isolation and deterministic verification.
- Risky actions require explicit human approval.

## Known v0.1.1 limits

- GitHub install is supported; PyPI publication is not done yet.
- Privacy scan is a guardrail, not a complete secret scanner.
- Hermes activation is manual by design; the kit prepares automation but does not activate it.
- `audit-report` checks the loop contract; it does not execute the real agent task.
- Target audience remains Hermes/agent power users comfortable with CLI and YAML.

## Release note

`v0.1.1` is suitable as a polished safety-first pre-runtime engineering kit for Hermes Agent loops, with CI-friendly promotion gates and cleaner package structure.
