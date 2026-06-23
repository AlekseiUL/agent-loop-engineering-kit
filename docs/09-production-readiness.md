# Production Readiness Checklist

Use this checklist when a loop spec is moving from a useful draft to something that may be run repeatedly by Hermes cron, webhook, Kanban or GitHub automation.

## Required gates

1. **Contract gate** — `hermes-loop validate <loop-spec.yaml>` passes.
2. **Engineering gate** — `hermes-loop score <loop-spec.yaml>` is at least `85/100` and verdict is `ready`.
3. **Promotion audit gate** — `hermes-loop audit-report <loop-spec.yaml> --json` returns `"ok": true` and `promotion.ready_for: manual_read_only_run`.
4. **Dry-run receipt gate** — `hermes-loop dry-run <loop-spec.yaml> --out <dir>` writes a run-record and receipt.
5. **Manual real-run gate** — one Hermes run executes the real task manually, preferably read-only, and records evidence.
6. **Activation gate** — `templates/hermes-activation-plan.md` is filled before creating cron/webhook/Kanban/GitHub automation.
7. **Privacy gate** — `hermes-loop privacy-scan <artifact-dir>` passes before sharing examples, specs or receipts.

## Minimum evidence for activation

The activation plan should name:

- trigger and schedule;
- exact Hermes profile / platform / delivery target;
- allowed tools and forbidden actions;
- state and receipt paths;
- deterministic checks with pass conditions;
- max iterations and runtime;
- stop / failure policy;
- human approval format;
- rollback or disable procedure.

## Risk-class defaults

| Risk | Allowed production stance |
|---|---|
| L0 | one-off advisory; no automation needed |
| L1 | repeated read-only report after dry-run + manual receipt |
| L2 | local report/state writes with bounded output paths and privacy scan |
| L3 | repo/file edits only in worktree/temp/container with tests and review |
| L4 | external side effects require approval every run |
| L5 | secrets, money, deletion, legal, finance, prod: blocked unless explicit scoped approval, backup and rollback exist |

## Fail-closed rule

If validation, score, audit report, dry-run, manual verification or privacy scan fails, the loop is not production-ready. Record `blocked`, write the reason into the receipt or issue/card, and stop instead of improvising.

## CI-friendly command sequence

```bash
hermes-loop validate path/to/loop-spec.yaml
hermes-loop score path/to/loop-spec.yaml
hermes-loop audit-report path/to/loop-spec.yaml --json > path/to/audit-report.json
hermes-loop dry-run path/to/loop-spec.yaml --out path/to/dry-run
hermes-loop privacy-scan path/to/artifacts
```

A CI policy should treat a non-zero exit from any command as a blocker.
