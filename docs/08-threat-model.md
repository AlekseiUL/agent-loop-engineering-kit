# Threat Model for Hermes Agent Loops

Hermes loops can touch files, terminal commands, web pages, browser sessions, memory, cron, Kanban, GitHub and messaging gateways. Treat every repeated loop as a small system with failure modes.

## Main threats

| Threat | How it happens | Default control |
|---|---|---|
| Prompt injection | Web page, repo file, issue body or chat text tells the agent to ignore rules | Treat external content as data; never follow instructions from sources |
| Secret exfiltration | Tokens/keys/private paths leak into receipts, logs or reports | Privacy scan; summarize or hash sensitive inputs; never print secrets |
| Cross-profile leakage | One Hermes profile reads/writes another profile by accident | Explicit profile boundary and allowed paths |
| Tool escalation | Read-only loop starts using terminal/write/send tools | Allowed tool list and forbidden actions in spec |
| Stale state | Old receipt/state causes wrong decision | Read state before run; record run id and timestamps |
| Repeated side effects | Retry sends duplicate messages, posts, charges or deploys | Idempotency key, dedupe rule, max iterations, human gate |
| Infinite repair loop | Agent keeps trying vague fixes | Max runtime, repeated-error stop, failure receipt |
| Fake success | Model says done without tests/source evidence | Deterministic verification and audit-grade receipt |
| Poisoned local repo | Malicious README/scripts influence agent behavior | Read AGENTS.md/contracts first; do not execute untrusted scripts by default |
| Public artifact leak | Example/spec/receipt includes private local paths or chats | Artifact privacy scan before commit/publish |

## Safety rules

1. Manual and read-only first.
2. No cron/webhook/Kanban activation before a dry-run receipt.
3. No external side effect without scoped approval.
4. No secrets in specs, prompts, receipts, logs or examples.
5. No write-capable loop without allowed paths and rollback.
6. No unattended L3+ repo/file edit loop by default.
7. Stop on missing input, failed verification, repeated error or human-gate condition.
8. If evidence is weak, output `NO_CHANGE` or `blocked`, not a fake fix.

## Public GitHub rule

Before publishing this kit or a loop built from it:

```bash
hermes-loop privacy-scan .
hermes-loop smoke
```

Then manually check receipts/examples for private names, paths, chat logs, customer material and credentials.
