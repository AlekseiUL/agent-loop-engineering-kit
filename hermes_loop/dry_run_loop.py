#!/usr/bin/env python3
"""Create a safe dry-run receipt for a Hermes loop spec.

This does not execute the user's agent task. It proves the loop contract can be
loaded, validated, scored, observed and rendered before anyone wires cron,
webhooks, Kanban or write-capable tools.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import jsonschema
import yaml

from importlib import resources

def resource_path(*parts: str):
    return resources.files("hermes_loop").joinpath("resources", *parts)

from hermes_loop import evaluate_loop_spec, render_loop_receipt, validate_loop_spec  # noqa: E402


def load_spec(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("loop spec must be a mapping")
    schema = json.loads(resource_path("schemas", "loop-spec.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(data, schema)
    rule_errors = validate_loop_spec.rules(data)
    if rule_errors:
        raise ValueError("loop spec failed validation: " + "; ".join(rule_errors))
    return data


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_run_record(spec: dict[str, Any], spec_path: Path, score: dict[str, Any]) -> dict[str, Any]:
    name = str(spec["name"])
    now_dt = datetime.now(timezone.utc)
    now = now_dt.strftime("%Y%m%dT%H%M%SZ")
    iso_now = now_dt.isoformat().replace("+00:00", "Z")
    trigger = spec.get("trigger", {}) if isinstance(spec.get("trigger"), dict) else {}
    verification = spec.get("verification", {}) if isinstance(spec.get("verification"), dict) else {}
    deterministic = verification.get("deterministic_checks") or []
    review = verification.get("review_checks") or []
    checks = [
        {
            "name": "loop_spec_validation",
            "result": "PASS",
            "evidence": f"{spec_path.as_posix()} passed schema and safety rules",
        },
        {
            "name": "loop_engineering_score",
            "result": str(score["score"]),
            "evidence": f"verdict={score['verdict']}; categories={score['category_scores']}",
        },
        {
            "name": "deterministic_checks_declared",
            "result": "PASS" if deterministic else "FAIL",
            "evidence": f"{len(deterministic)} deterministic check(s) declared",
        },
        {
            "name": "human_gate_declared",
            "result": "PASS",
            "evidence": ", ".join(spec.get("human_gate", {}).get("required_for", [])),
        },
    ]
    if review:
        checks.append(
            {
                "name": "review_checks_declared",
                "result": "PASS",
                "evidence": f"{len(review)} review check(s) declared",
            }
        )
    return {
        "loop_name": name,
        "run_id": f"dry-run-{name}-{now}",
        "status": "DRY_RUN",
        "trigger": f"dry_run_cli:{trigger.get('type', 'unknown')}",
        "started_at": iso_now,
        "ended_at": iso_now,
        "hermes_profile": "not_applicable_dry_run",
        "agent_version": None,
        "loop_spec_version": str(spec.get("schema_version", "unknown")),
        "input_summary": f"Contract dry run for {spec_path.as_posix()}; task inputs were not executed.",
        "input_hashes": [],
        "tool_calls": [],
        "commands_run": [],
        "changed_files": [],
        "approval_events": [],
        "redactions": [],
        "rollback_available": False,
        "rollback": None,
        "actions_taken": [
            "loaded loop spec",
            "validated schema and safety rules",
            "scored loop-engineering usefulness",
            "rendered dry-run receipt",
            "did not execute agent task or external side effects",
        ],
        "verification": checks,
        "stop_reason": "dry_run_contract_verified_no_task_execution",
        "artifacts": [],
        "risks": [
            "dry run does not prove live task quality",
            "run one manual read-only real execution before scheduling automation",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("loop_spec")
    parser.add_argument("--run-record-out", required=True)
    parser.add_argument("--receipt-out", required=True)
    parser.add_argument("--min-score", type=int, default=85)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    spec_path = Path(args.loop_spec)
    run_record_out = Path(args.run_record_out)
    receipt_out = Path(args.receipt_out)
    try:
        spec = load_spec(spec_path)
        score = evaluate_loop_spec.score_spec(spec)
        if int(score["score"]) < args.min_score:
            raise ValueError(f"loop score {score['score']} is below min-score {args.min_score}")
        record = build_run_record(spec, spec_path, score)
        record["artifacts"] = [run_record_out.as_posix(), receipt_out.as_posix()]
        render_loop_receipt.validate_run_record(record)
        write_text(run_record_out, yaml.safe_dump(record, sort_keys=False, allow_unicode=True))
        write_text(receipt_out, render_loop_receipt.render(record))
    except Exception as exc:
        if args.json:
            print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        else:
            print(f"FAIL dry run: {exc}", file=sys.stderr)
        return 1

    result = {
        "ok": True,
        "score": score["score"],
        "verdict": score["verdict"],
        "run_record": run_record_out.as_posix(),
        "receipt": receipt_out.as_posix(),
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"PASS dry run {spec['name']} score={score['score']} verdict={score['verdict']}")
        print(f"run_record={run_record_out}")
        print(f"receipt={receipt_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
