# GitHub Coding Loop

Use this pattern when a Hermes-based agent handles repo maintenance, bug fixes or small implementation tasks.

```text
GitHub issue/request -> intake -> isolated worktree -> maker run -> tests/lint -> independent verifier -> PR/report -> receipt
```

## Minimal loop spec choices

| Block | Recommended value |
|---|---|
| trigger | `github_issue`, `kanban` or manual chat for the first runs |
| state | issue comment, Kanban card or receipt file |
| tools | read/search files, terminal tests, patch/write only inside worktree |
| isolation | `git_worktree` for L3 changes |
| verification | unit tests, lint/build, smoke command, diff review |
| human gate | public push/PR, merge, deploy, secrets, deletion |
| receipt | changed files, commands run, test output, remaining risk |

## Do not trust

- model self-report without diff/test evidence;
- a green test run that did not touch the changed path;
- auto-push or auto-merge as a default;
- broad refactors without rollback;
- missing `AGENTS.md` / local repo instructions.

## Release gate

Before a coding loop is considered useful, the receipt must show:

1. exact input request;
2. allowed and forbidden paths;
3. diff summary;
4. commands run with exit codes;
5. failed checks if any;
6. reviewer/verifier result;
7. rollback path.

If the loop cannot produce that receipt, it is not ready for unattended use.
