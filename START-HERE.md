# Start Here

Agent Loop Engineering Kit helps you turn a repeated Hermes Agent request into a bounded loop contract **before** you automate it.

Prompt = instruction for one pass.

Loop = repeatable work process with state, checks, brakes and receipt.

## 0. Install

You need Python 3.11+ and one installer.

Recommended:

```bash
uv tool install https://github.com/AlekseiUL/agent-loop-engineering-kit.git
hermes-loop --help
```

If you do not have `uv`, install it from <https://docs.astral.sh/uv/> or use `pipx`:

```bash
pipx install git+https://github.com/AlekseiUL/agent-loop-engineering-kit.git
```

## 1. The first useful loop

Start with something read-only, for example a daily briefing:

```text
Every morning, read the configured project sources and produce a short briefing with sources, open questions and risks.
```

Do **not** begin with cron. First prove the contract.

## 2. Create a spec

```bash
hermes-loop init /tmp/daily-briefing-loop.yaml
```

Open the file and fill the fields. Keep it read-only at first.

The eight blocks:

1. Trigger — what starts it.
2. Inputs — what it needs.
3. State — what it remembers outside model context.
4. Context assembly — what gets loaded into this run.
5. Tools — what it may use.
6. Isolation — where it can safely act.
7. Verification — how reality is checked.
8. Stop / human gate / receipt — how it ends.

## 3. Validate and score

```bash
hermes-loop validate /tmp/daily-briefing-loop.yaml
hermes-loop score /tmp/daily-briefing-loop.yaml
```

If the score is low, fix the spec before running anything in Hermes.

## 4. Dry-run the contract

```bash
hermes-loop dry-run /tmp/daily-briefing-loop.yaml --out /tmp/daily-briefing-run
hermes-loop render-receipt /tmp/daily-briefing-run/run-record.yaml
```

This creates a run-record and receipt. It does **not** execute the real agent task.

## 5. Then run it manually in Hermes

Paste the loop spec into a Hermes chat and ask for a manual read-only run:

```text
Use this loop spec as the contract for one manual read-only run.
Do not create cron/webhook/Kanban jobs.
Do not write to Hermes memory, skills, cron or config.
Return: inputs used, tools/actions taken, verification output, stop reason, unresolved risks and receipt path.

<attach or paste loop-spec.yaml>
```

If that manual run is clean, then write an activation plan. Cron/webhook/Kanban comes later.

## Before automation

Your loop must say:

- where state lives;
- which tools are allowed;
- which actions are forbidden;
- how result is verified;
- when it stops;
- when it asks a human;
- where the receipt is written;
- how to disable or roll back the loop.

If you cannot verify, stop, and investigate it from a receipt, it is too early to automate.
