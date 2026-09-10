#!/usr/bin/env python3
"""Build a machine-readable promotion audit for a Hermes loop spec."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import jsonschema

from hermes_loop import evaluate_loop_spec, validate_loop_spec


READY_FOR = "manual_read_only_run"
FIX_CONTRACT = "fix_loop_contract"


def _schema_errors(spec: dict[str, Any]) -> list[str]:
    schema = json.loads(validate_loop_spec.resource_path("schemas", "loop-spec.schema.json").read_text(encoding="utf-8"))
    try:
        jsonschema.validate(spec, schema)
    except jsonschema.ValidationError as exc:
        return [exc.message]
    return []


def build_report(path: str, min_score: int = 85) -> dict[str, Any]:
    errors: list[str] = []
    spec: dict[str, Any] = {}
    try:
        spec = validate_loop_spec.load(path)
    except Exception as exc:  # pragma: no cover - defensive CLI edge
        errors.append(str(exc))

    if spec:
        errors.extend(_schema_errors(spec))
        if not errors:
            errors.extend(validate_loop_spec.rules(spec))

    score = evaluate_loop_spec.score_spec(spec) if spec else {
        "score": 0,
        "max_score": 100,
        "verdict": "error",
        "category_scores": {},
        "findings": ["spec could not be loaded"],
    }
    score_value = int(score.get("score", 0))
    score_ready = score_value >= min_score and score.get("verdict") == "ready"
    blockers = list(errors)
    if not score_ready:
        blockers.append(f"loop score {score_value} is below required ready threshold {min_score} or verdict is {score.get('verdict')}")
    ok = not blockers
    return {
        "path": path,
        "ok": ok,
        "validation": {"ok": not errors, "errors": errors},
        "score": score,
        "promotion": {
            "ready_for": READY_FOR if ok else FIX_CONTRACT,
            "min_score": min_score,
            "blocked_by": blockers,
        },
        "next_steps": _next_steps(ok),
    }


def _next_steps(ok: bool) -> list[str]:
    if ok:
        return [
            "Run one manual read-only Hermes execution using this loop spec as the contract.",
            "Record inputs, tool actions, deterministic verification output, stop reason and receipt path.",
            "Only after a clean manual receipt, write an activation plan for cron/webhook/Kanban/GitHub automation.",
        ]
    return [
        "Fix validation errors and score findings before any real agent run.",
        "Re-run hermes-loop audit-report until promotion.ready_for is manual_read_only_run.",
        "Do not create cron/webhook/Kanban/GitHub automation from this spec yet.",
    ]


def render_markdown(report: dict[str, Any]) -> str:
    score = report["score"]
    lines = [
        "# Loop Promotion Audit Report",
        "",
        f"- Path: `{report['path']}`",
        f"- Status: `{'PASS' if report['ok'] else 'BLOCKED'}`",
        f"- Score: `{score.get('score')}/{score.get('max_score', 100)}`",
        f"- Verdict: `{score.get('verdict')}`",
        f"- Ready for: `{report['promotion']['ready_for']}`",
        "",
        "## Validation",
        "",
    ]
    errors = report["validation"]["errors"]
    lines.extend(["- PASS"] if not errors else [f"- {error}" for error in errors])
    lines += ["", "## Score findings", ""]
    findings = score.get("findings") or []
    lines.extend(["- none"] if not findings else [f"- {finding}" for finding in findings])
    lines += ["", "## Promotion blockers", ""]
    blockers = report["promotion"]["blocked_by"]
    lines.extend(["- none"] if not blockers else [f"- {blocker}" for blocker in blockers])
    lines += ["", "## Next steps", ""]
    lines.extend(f"- {step}" for step in report["next_steps"])
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a promotion audit report for a Hermes loop spec.")
    parser.add_argument("loop_spec")
    parser.add_argument("--min-score", type=int, default=85)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON instead of Markdown")
    parser.add_argument("--out", help="Write report to this path instead of stdout")
    args = parser.parse_args(argv)

    report = build_report(args.loop_spec, min_score=args.min_score)
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n" if args.json else render_markdown(report)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
