---
name: agent-loop-engineering
description: Design bounded Hermes agent loops with state, verification, human gates and receipts.
---

# Agent Loop Engineering Skill

Use this when a Hermes user wants to turn repeated agent work into a safe loop.

## Operating sequence

1. Start with the loose task in plain language.
2. Classify risk: L0 advisory, L1 repeated read-only, L2 local writes, L3 repo/file edits, L4 external side effects, L5 money/secrets/deletion/legal/prod.
3. Fill `templates/loop-spec.yaml` before creating cron/webhook/Kanban automation.
4. Validate the spec:
   ```bash
   python scripts/validate_loop_spec.py path/to/loop-spec.yaml
   ```
5. Score practical usefulness:
   ```bash
   python scripts/evaluate_loop_spec.py path/to/loop-spec.yaml
   ```
6. Run manually and read-only first. Save a run record and receipt.
7. Automate only after the receipt proves the loop stops, verifies and escalates correctly.

## Hard brakes

Do not publish, deploy, delete, access secrets, change billing, create scheduled jobs or weaken safety rules without explicit scoped approval.

## Definition of done

A loop is ready only when it has:

- trigger, inputs, state and context rules;
- allowed tools and forbidden actions;
- isolation mode;
- deterministic verification;
- review checks where judgement is needed;
- max iterations and runtime;
- human gate format;
- receipt path and readable receipt;
- privacy scan clean for shared/public artifacts.
