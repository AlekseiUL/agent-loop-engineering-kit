# Bad Loop Examples

These examples should fail validation or scoring. They exist to show that the kit blocks unsafe loop shapes, not only that good examples pass.

Run:

```bash
hermes-loop validate examples/bad-cron-repo-editor/loop-spec.yaml
hermes-loop score examples/bad-cron-repo-editor/loop-spec.yaml
```

Expected: validation fails because an L3 repo-editing loop is cron-triggered and lacks safe isolation/verification.
