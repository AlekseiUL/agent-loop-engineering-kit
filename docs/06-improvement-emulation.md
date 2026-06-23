# Improvement Emulation

This kit should prove one thing: a Hermes user gets a safer and more useful loop than a loose prompt.

Use the evaluator before scheduling or delegating a loop:

```bash
python scripts/evaluate_loop_spec.py examples/emulation-prompt-only.yaml examples/daily-briefing-loop/loop-spec.yaml
```

Expected shape:

```text
  0-30/100  not_loop_engineered  prompt-only or vague request
 60-84/100  needs_work           usable draft, still has gaps
 85-100/100 ready                bounded loop with safety, verification and receipts
```

## What the score checks

| Area | Meaning |
|---|---|
| Contract | The loop has trigger, inputs, state, tools, isolation, gates, outputs and receipt. |
| Safety | Dangerous actions are forbidden by default and require scoped approval. |
| Verification | The loop has deterministic checks, review checks and a definition of done. |
| Observability | State, artifacts and receipts make the run inspectable after the model is gone. |
| Hermes fit | Trigger/state/tools map to normal Hermes surfaces: manual, cron, webhook, Kanban, files, reports. |
| Operability | Runtime limits, max iterations, success signal and failure policy are explicit. |

## How to use it in practice

1. Write a loose task as `examples/emulation-prompt-only.yaml` or a scratch file.
2. Convert it into a real `loop-spec.yaml` using `templates/loop-spec.yaml`.
3. Run validator + evaluator.
4. Fix the lowest category before automation.
5. Only then consider cron/webhook/Kanban activation.

The evaluator is intentionally conservative. It does not prove the loop is good forever. It catches missing brakes before the loop starts acting like it has a driver's license.
