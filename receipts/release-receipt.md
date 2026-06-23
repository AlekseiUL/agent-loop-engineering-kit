# Release Receipt

## Product

Agent Loop Engineering Kit

## Release

- Version: `0.1.0`
- Status: `public v0.1`
- Repository: <https://github.com/AlekseiUL/agent-loop-engineering-kit>
- Commit: `8d06400 feat: publish agent loop engineering kit v0.1`

## Release contract

`v0.1` is a design, validation, dry-run, receipt and privacy-scan kit for Hermes Agent loop contracts.

It is not a Hermes runtime, scheduler, cron manager, webhook runner, or proof that model output is true.

## What is included

- README with English and Russian product explanation.
- Hero image under `assets/agent-loop-engineering-kit-hero.jpg`.
- `START-HERE.md` first-user path.
- Hermes-first docs and lifecycle guide.
- Threat model.
- Loop spec JSON schema with `schema_version: "1.0"`.
- Run-record and receipt schema contract v1.
- Templates: loop spec, activation plan, verification contract, human gate policy, receipt.
- Examples:
  - daily briefing loop;
  - Hermes cron daily briefing promotion path;
  - repo maintenance loop;
  - coding fix loop;
  - research watchlist loop;
  - diagnostic loop;
  - deliberately unsafe cron repo editor example.
- Installable `hermes-loop` CLI.
- Scripts:
  - `scripts/validate_loop_spec.py`;
  - `scripts/evaluate_loop_spec.py`;
  - `scripts/dry_run_loop.py`;
  - `scripts/render_loop_receipt.py`;
  - `scripts/scan_loop_privacy.py`;
  - `scripts/smoke.sh`;
  - `scripts/installed_cli_smoke.sh`.
- Pytest regression suite.
- GitHub Actions smoke workflow.
- Portable single-file kit under `kit/`.

## Verification run

Public release verification was run from a GitHub install and repository checkout.

```bash
pip install git+https://github.com/AlekseiUL/agent-loop-engineering-kit.git
hermes-loop --help
hermes-loop init /tmp/agent-loop-public-loop.yaml
hermes-loop validate /tmp/agent-loop-public-loop.yaml
hermes-loop dry-run /tmp/agent-loop-public-loop.yaml --out /tmp/agent-loop-public-github-out
pytest -q
bash scripts/smoke.sh
bash scripts/installed_cli_smoke.sh
hermes-loop privacy-scan .
```

## Result

- Public GitHub install: PASS.
- CLI help/init/validate/dry-run: PASS.
- Good example validation: PASS.
- Deliberately bad L3 cron repo editor: blocked as expected.
- Receipt rendering: PASS.
- Privacy scan: PASS.
- Tests: `22 passed`.
- Installed CLI smoke: PASS.
- GitHub Actions smoke: PASS.

## Safety position

- No always-on cron by default.
- No auto-push.
- No auto-merge.
- No deploy.
- No public posting.
- No secret access.
- No writes to Hermes memory, skills, cron, plugins, config or auth by default.
- Cross-profile access requires explicit approval.
- L3 coding loops require isolation and deterministic verification.
- Risky actions require explicit human approval.

## Known v0.1 limits

- GitHub install is supported; PyPI publication is not done yet.
- Privacy scan is a guardrail, not a complete secret scanner.
- Hermes activation is manual by design; the kit prepares automation but does not activate it.
- Target audience for v0.1 is Hermes/agent power users comfortable with CLI and YAML.

## Release note

Public v0.1 is suitable as a safety-first pre-runtime engineering kit for Hermes Agent loops.
