# Release Receipt

## Product

Hermes Agent Loop Kit

## Status

`draft-pilot`, GitHub-ready local scaffold.

Not published.

## What is included

- README and START-HERE beginner path.
- Hermes-first docs.
- Loop spec JSON schema.
- Run-record and receipt schemas.
- Templates: loop spec, verification contract, human gate policy, receipt.
- Examples:
  - daily briefing loop;
  - repo maintenance loop;
  - coding fix loop;
  - research watchlist loop;
  - diagnostic loop.
- Scripts:
  - `scripts/validate_loop_spec.py`;
  - `scripts/render_loop_receipt.py`;
  - `scripts/scan_loop_privacy.py`;
  - `scripts/smoke.sh`.
- Pytest smoke tests.
- Portable single-file kit under `kit/`.

## Verification run

```bash
python scripts/validate_loop_spec.py examples/*/loop-spec.yaml
python scripts/render_loop_receipt.py examples/daily-briefing-loop/run-record.yaml > receipts/daily-briefing.receipt.md
python scripts/render_loop_receipt.py examples/repo-maintenance-loop/run-record.yaml > receipts/repo-maintenance.receipt.md
python scripts/scan_loop_privacy.py .
pytest -q
```

## Result

- Example validation: PASS, 5/5 examples.
- Receipt rendering: PASS, 2 receipts generated.
- Privacy scan: PASS.
- Tests: PASS, 7 passed.

## Safety position

- No always-on cron by default.
- No auto-push.
- No auto-merge.
- No deploy.
- No public posting.
- No secret access.
- L3 coding loops require isolation and deterministic verification.
- Risky actions require explicit human approval.

## Release note

This is ready as a local GitHub-ready draft. It still needs final public-review pass before publishing to an external GitHub repository.
