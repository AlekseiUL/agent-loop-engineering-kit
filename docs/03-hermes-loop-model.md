# Hermes Loop Model

Hermes already has the pieces of a loop: profiles, skills, memory, files, terminal tools, browser tools, cron, webhooks, Kanban and GitHub workflows. Loop engineering is the contract that decides how those pieces are allowed to repeat.

A useful loop is not just `run this prompt every day`.

```text
trigger -> context/state -> agent/tool run -> observe -> verify -> update state -> stop/retry/escalate -> receipt
```

## Mapping to Hermes

| Loop block | Hermes surface | Design question |
|---|---|---|
| Trigger | manual chat, cronjob, webhook, Kanban card, GitHub issue | What starts the run, and should it be manual first? |
| Inputs | files, URLs, issue body, chat request, repo path | What must exist before the run is allowed to start? |
| State | local file, receipt, Kanban card, issue comment, database | What survives after model context disappears? |
| Context assembly | AGENTS.md, skills, wiki/docs, session search, selected files | What gets loaded, and what is intentionally excluded? |
| Tools | Hermes toolsets: file, terminal, browser, web, GitHub, cron, Kanban | Which actions are allowed for this loop? |
| Isolation | read-only, temp dir, git worktree, profile boundary, container | Where can damage happen if the agent is wrong? |
| Verification | tests, lint, schema validation, smoke, reviewer, source check | What proves reality changed or stayed safe? |
| Stop/gate | max iterations, timeout, failure policy, human approval | When does the loop stop instead of improvising? |
| Receipt | Markdown/YAML report, PR comment, Kanban update | Can a human audit the run later? |

## Practical rule

For Hermes systems, the safest progression is:

1. manual read-only task;
2. manual loop with receipt;
3. scheduled read-only loop;
4. write-capable loop in isolated workspace;
5. external side-effect loop only with explicit per-run approval.

Skipping steps is how a harmless helper becomes a tiny unattended incident generator.
