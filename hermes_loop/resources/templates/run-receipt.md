# Audit-grade Run Receipt v1

Every real loop run should leave a receipt that can be investigated after the model context is gone.

## Required fields

- `loop_name`
- `run_id`
- `status`
- `trigger`
- `started_at`
- `ended_at`
- `hermes_profile`
- `loop_spec_version`
- `input_summary`
- `actions_taken`
- `verification`
- `stop_reason`
- `rollback_available`

## Recommended fields

- `agent_version`
- `input_hashes`
- `tool_calls`
- `commands_run`
- `changed_files`
- `approval_events`
- `redactions`
- `rollback`
- `artifacts`
- `risks`

## Example skeleton

```yaml
loop_name: example-loop
run_id: example-loop-20260623T120000Z
status: DRY_RUN
trigger: manual dry run
started_at: "2026-06-23T12:00:00Z"
ended_at: "2026-06-23T12:01:00Z"
hermes_profile: default
agent_version: unknown
loop_spec_version: "1.0"
input_summary: "Dry-run validation of example-loop; no private inputs included."
input_hashes: []
actions_taken:
  - loaded loop spec
  - validated schema and safety rules
tool_calls: []
commands_run:
  - command: python scripts/validate_loop_spec.py examples/example-loop/loop-spec.yaml
    exit_code: 0
    evidence: PASS
verification:
  - name: spec_validation
    result: PASS
    evidence: validate_loop_spec.py exited 0
stop_reason: dry_run_contract_verified_no_task_execution
changed_files: []
approval_events: []
redactions: []
rollback_available: false
rollback: null
artifacts:
  - /tmp/example-loop/receipt.md
risks:
  - dry run does not prove live task quality
```

## Receipt rules

- Do not include secrets, cookies, raw private chat logs or customer data.
- Use hashes/summaries for sensitive inputs.
- Record failed checks. A failed receipt is still useful evidence.
- For write-capable loops, `rollback_available` should be true or the loop should stop before writing.
