# Safety Gates

Safety gates are the brakes of the loop. If a loop can repeat, it needs explicit stop rules before it needs more clever prompting.

## Always approval-gated

Require scoped human approval before:

- deleting files or user data;
- reading, printing or moving secrets;
- public posting or sending from a user's account;
- production deploys or broad service restarts;
- payments, billing, renewals or purchases;
- legal/finance commitments;
- weakening the loop's own safety rules.

Approval should name the action, scope and rollback:

```text
APPROVE LOOP ACTION: <action> / <scope> / <rollback>
```

## Risk classes

| Class | Default stance | Required brakes |
|---|---|---|
| L0 advisory | one-off manual | cite uncertainty |
| L1 repeated read-only | dry-run then schedule | source list, receipt, timeout |
| L2 local reports/state | active with receipt | privacy scan, bounded write paths |
| L3 repo/file edits | isolated worktree | tests, diff, reviewer, rollback |
| L4 external side effects | approval every run | explicit approval and receipt |
| L5 secrets/money/deletion/legal/prod | blocked by default | explicit approval, backup, rollback, second check |

## Failure policy

A good loop stops when:

- required input is missing;
- verification fails;
- the same error repeats;
- it reaches max iterations/runtime;
- it touches a forbidden action;
- it needs human approval.

Do not let the model "try something else" forever. Symptom is not cause; repeated guessing is just automated damage.
