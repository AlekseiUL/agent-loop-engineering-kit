#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
RISK = {"L0": 0, "L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5}
DANGER_ALIASES = {
    "deletion": {"deletion", "delete_files", "delete_data"},
    "secrets": {"secrets", "access_secrets", "print_secrets"},
    "public_posting": {"public_posting", "send_messages", "post_publicly"},
    "production_deploy": {"production_deploy", "deploy_production", "restart_services"},
    "payments": {"payments", "billing", "purchase"},
}
DANGER = set(DANGER_ALIASES)


def load(path: str) -> dict[str, Any]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("spec must be a mapping")
    return data


def obj(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def missing_danger_coverage(values: set[str]) -> list[str]:
    return sorted(name for name, aliases in DANGER_ALIASES.items() if not (values & aliases))


def rules(spec: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    risk_class = spec.get("risk_class")
    lvl = RISK.get(risk_class if isinstance(risk_class, str) else "", -1)
    stop = obj(spec.get("stop_conditions"))
    if not stop.get("success_signal"):
        errors.append("missing stop_conditions.success_signal")
    if not stop.get("failure_policy"):
        errors.append("missing stop_conditions.failure_policy")
    if stop.get("max_iterations", 0) > 3 and lvl >= 1 and not stop.get("rationale"):
        errors.append("max_iterations above 3 needs stop_conditions.rationale")

    verification = obj(spec.get("verification"))
    if not (verification.get("deterministic_checks") or verification.get("review_checks")):
        errors.append("missing verification checks")
    if lvl >= 3 and not verification.get("deterministic_checks"):
        errors.append("L3+ requires deterministic verification")

    isolation_mode = obj(spec.get("isolation")).get("mode")
    if lvl >= 3 and isolation_mode not in {"git_worktree", "temp_dir", "container", "profile_boundary"}:
        errors.append("L3+ requires real isolation")

    tools = obj(spec.get("tools"))
    gates = obj(spec.get("human_gate"))
    forbidden = set(tools.get("forbidden_actions") or [])
    required_for = set(gates.get("required_for") or [])
    missing_forbidden = missing_danger_coverage(forbidden)
    missing_gates = missing_danger_coverage(required_for)
    if missing_forbidden:
        errors.append("forbidden_actions missing dangerous actions: " + ", ".join(missing_forbidden))
    if missing_gates:
        errors.append("human gates missing dangerous actions: " + ", ".join(missing_gates))

    if obj(spec.get("receipt")).get("required") is not True:
        errors.append("receipt.required must be true")
    if obj(spec.get("trigger")).get("type") == "cron" and lvl >= 3:
        errors.append("cron-triggered L3+ blocked by default")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    schema = json.loads((ROOT / "schemas/loop-spec.schema.json").read_text(encoding="utf-8"))
    out = []
    ok_all = True
    for raw in args.paths:
        errors: list[str] = []
        try:
            spec = load(raw)
            jsonschema.validate(spec, schema)
            errors += rules(spec)
        except Exception as exc:
            errors.append(str(exc))
        ok = not errors
        ok_all = ok_all and ok
        out.append({"path": raw, "ok": ok, "errors": errors})
    if args.json:
        print(json.dumps({"ok": ok_all, "results": out}, ensure_ascii=False, indent=2))
    else:
        for result in out:
            print(("PASS" if result["ok"] else "FAIL"), result["path"])
            for error in result["errors"]:
                print("  -", error)
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main())
