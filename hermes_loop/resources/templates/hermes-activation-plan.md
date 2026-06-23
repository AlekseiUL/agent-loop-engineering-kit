# Hermes Activation Plan

Use this before turning a loop spec into a live Hermes cron, webhook, Kanban or GitHub workflow.

Hard rule: **manual first, cron/webhook/Kanban later**. A scheduled or event-driven loop needs a passing dry-run receipt and at least one clean manual run.

## Identity

- Loop name:
- Owner:
- Reviewer:
- Hermes profile:
- Lifecycle stage: `draft | dry_run | active_manual | active_scheduled | paused | deprecated`
- Risk class:

## Activation target

- Surface: `manual | cron | webhook | kanban | github_issue`
- Trigger details:
- Disable switch:
- State path:
- Receipt path:

## Hermes profile boundary

- Allowed Hermes profile:
- Forbidden Hermes profiles:
- Allowed profile-local read paths:
- Allowed profile-local write paths:
- Forbidden profile writes: `memory | skills | cron | plugins | config | auth`
- Cross-profile access approval rule:

Default: no cross-profile access and no writes to Hermes memory, skills, cron, plugins, config or auth unless this plan explicitly allows the action and a human approves it.

## Boundaries

- Allowed tools/toolsets:
- Forbidden actions:
- Allowed read paths:
- Allowed write paths:
- Network policy:
- Data classification: `public | internal | private | secret`
- Secrets policy:

## Verification

- Deterministic checks:
- Review checks:
- Definition of done:
- Smoke command:
- Privacy scan command:

## Operations

- Max iterations:
- Max runtime:
- Retry/backoff:
- Idempotency key or dedupe rule:
- Concurrency rule:
- Escalation condition:

## Human gate

Approval format:

```text
APPROVE LOOP ACTION: <action> / <scope> / <rollback> / <expires>
```

Approval required for:

- deletion;
- secrets;
- public posting/sending;
- production deploy/restart;
- payments/billing;
- legal/finance commitment;
- safety-rule change;
- cross-profile access;
- Hermes memory/skill/cron/config writes.

## Rollback

- Backup/checkpoint procedure:
- Rollback procedure:
- Owner who can roll back:
- Evidence that rollback was tested:

## Activation checklist

- [ ] `hermes-loop validate <spec>` passes.
- [ ] `hermes-loop score <spec>` is acceptable for lifecycle stage.
- [ ] `hermes-loop dry-run <spec> --out <tmp>` produces a valid receipt.
- [ ] One manual read-only real run completed.
- [ ] Receipt is audit-grade and privacy-scanned.
- [ ] Disable procedure is documented and tested.
- [ ] Human approval exists for any external/write/prod/cross-profile action.
- [ ] Scheduled/event-driven activation is still necessary after manual proof.
