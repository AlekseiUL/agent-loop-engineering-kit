# Hermes Lifecycle: From Prompt to Safe Loop

This is the practical path for a Hermes user. Do not start with cron. Start with proof.

## 1. Direct task

Use a normal Hermes chat when the work is one-off or advisory.

```text
Inspect this repo and write a read-only maintenance report.
```

If the same request repeats, promote it to a loop spec.

## 2. Loop spec

Copy `templates/loop-spec.yaml` and fill:

- trigger;
- required inputs;
- durable state;
- allowed tools;
- forbidden actions;
- isolation;
- deterministic verification;
- stop conditions;
- human gates;
- receipt path.

Validate and score:

```bash
python scripts/validate_loop_spec.py path/to/loop-spec.yaml
python scripts/evaluate_loop_spec.py path/to/loop-spec.yaml
```

## 3. Contract dry run

Before running the real agent task, prove the contract can produce an audit artifact:

```bash
python scripts/dry_run_loop.py path/to/loop-spec.yaml \
  --run-record-out /tmp/loop-run-record.yaml \
  --receipt-out /tmp/loop-receipt.md
```

This does **not** execute the task. It checks that the loop is bounded, scored, gated and receipt-capable.

## 4. Manual read-only real run

Run the real Hermes task manually with the loop spec in context. Keep tools read-only unless the risk class explicitly allows writes.

The final answer or artifact must include:

- what inputs were used;
- what tools/actions happened;
- deterministic verification output;
- stop reason;
- receipt path;
- unresolved risk.

## 5. Automation promotion gate

Only after a clean manual run, consider automation.

| Target | Extra gate |
|---|---|
| `cronjob` | fresh-session prompt is self-contained; receipt delivery works; timeout set |
| `webhook` | payload schema and auth boundary documented |
| `kanban` | card has assignee, allowed paths, forbidden paths, verification and expected summary |
| `github_issue` | worktree isolation and no auto-merge/default push |

## 6. Stop or rollback

Stop instead of improvising when:

- required input is missing;
- source access fails;
- verification fails;
- the same error repeats;
- max iterations/runtime is reached;
- a forbidden action is needed;
- approval is required.

For write-capable loops, create a backup/checkpoint before apply and record rollback instructions in the receipt.
