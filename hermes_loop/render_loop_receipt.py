#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import jsonschema
import yaml

from importlib import resources

def resource_path(*parts: str):
    return resources.files("hermes_loop").joinpath("resources", *parts)



def validate_run_record(record: dict[str, Any]) -> None:
    schema = json.loads(resource_path("schemas", "loop-run-record.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(record, schema)


def table(items: list[dict[str, Any]], columns: list[str]) -> list[str]:
    lines = ["| " + " | ".join(columns) + " |", "|" + "|".join("---" for _ in columns) + "|"]
    for item in items:
        lines.append("| " + " | ".join(str(item.get(col, "")).replace("\n", " ") for col in columns) + " |")
    return lines


def bullets(items: list[Any]) -> list[str]:
    return [f"- {item}" for item in items] if items else ["- none"]


def render(record: dict[str, Any]) -> str:
    lines = [
        "# Loop Run Receipt",
        "",
        "## Identity",
        "",
        f"- Loop: `{record['loop_name']}`",
        f"- Run ID: `{record['run_id']}`",
        f"- Status: `{record['status']}`",
        f"- Trigger: {record['trigger']}",
        f"- Started: {record['started_at']}",
        f"- Ended: {record['ended_at']}",
        f"- Hermes profile: `{record['hermes_profile']}`",
        f"- Agent version: `{record.get('agent_version') or 'unknown'}`",
        f"- Loop spec version: `{record['loop_spec_version']}`",
        "",
        "## Input summary",
        "",
        record["input_summary"],
        "",
    ]
    if record.get("input_hashes"):
        lines += ["## Input hashes", "", *table(record["input_hashes"], ["name", "hash"]), ""]

    lines += ["## Actions taken", "", *bullets(record["actions_taken"]), ""]
    if record.get("tool_calls"):
        lines += ["## Tool calls", "", *table(record["tool_calls"], ["tool", "purpose", "result"]), ""]
    if record.get("commands_run"):
        lines += ["## Commands run", "", *table(record["commands_run"], ["command", "exit_code", "evidence"]), ""]

    lines += ["## Verification", "", *table(record["verification"], ["name", "result", "evidence"]), ""]
    lines += ["## Stop reason", "", record["stop_reason"], ""]
    lines += ["## Changed files", "", *bullets(record.get("changed_files") or []), ""]
    lines += ["## Approval events", ""]
    approvals = record.get("approval_events") or []
    if approvals:
        lines += table(approvals, ["action", "scope", "status", "rollback", "expires_at"])
    else:
        lines += ["- none"]
    lines += [""]
    lines += ["## Redactions", "", *bullets(record.get("redactions") or []), ""]
    lines += ["## Rollback", "", f"- Available: {record['rollback_available']}", f"- Procedure: {record.get('rollback') or 'none'}", ""]
    lines += ["## Artifacts", "", *bullets(record.get("artifacts") or []), ""]
    lines += ["## Risks / notes", "", *bullets(record.get("risks") or ["none recorded"])]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_record")
    args = parser.parse_args(argv)
    record = yaml.safe_load(Path(args.run_record).read_text(encoding="utf-8"))
    if not isinstance(record, dict):
        print("run record must be mapping", file=sys.stderr)
        return 1
    try:
        validate_run_record(record)
    except jsonschema.ValidationError as exc:
        print(f"invalid run record: {exc.message}", file=sys.stderr)
        return 1
    print(render(record), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
