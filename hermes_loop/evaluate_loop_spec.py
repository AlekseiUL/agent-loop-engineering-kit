#!/usr/bin/env python3
"""Score whether a Hermes loop spec is operationally useful, not only valid.

The validator answers: "does this match the contract?"
The evaluator answers: "would this probably improve an agent loop versus a loose prompt?"
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]

WEIGHTS = {
    "contract": 20,
    "safety": 20,
    "verification": 20,
    "observability": 15,
    "hermes_fit": 15,
    "operability": 10,
}

DANGERS = {"deletion", "secrets", "public_posting", "production_deploy", "payments"}
FORBIDDEN_DANGER_ALIASES = {
    "deletion": {"deletion", "delete_files", "delete_data"},
    "secrets": {"secrets", "access_secrets", "print_secrets"},
    "public_posting": {"public_posting", "send_messages", "post_publicly"},
    "production_deploy": {"production_deploy", "deploy_production", "restart_services"},
    "payments": {"payments", "billing", "purchase"},
}
HERMES_TRIGGERS = {"manual", "cron", "webhook", "kanban", "github_issue", "file_change"}
HERMES_STATE = {"file", "kanban", "github_issue", "database", "receipt"}
REAL_ISOLATION = {"read_only", "temp_dir", "git_branch", "git_worktree", "profile_boundary", "container"}


def load_yaml(path: str) -> dict[str, Any]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and any(str(x).strip() for x in value)


def _object(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _covers_dangers(values: set[str]) -> bool:
    return all(values & aliases for aliases in FORBIDDEN_DANGER_ALIASES.values())


def score_spec(spec: dict[str, Any]) -> dict[str, Any]:
    findings: list[str] = []
    scores = {key: 0 for key in WEIGHTS}

    required_top = [
        "name",
        "goal",
        "risk_class",
        "trigger",
        "inputs",
        "state",
        "tools",
        "isolation",
        "verification",
        "stop_conditions",
        "human_gate",
        "outputs",
        "receipt",
    ]
    present = sum(1 for key in required_top if key in spec and spec.get(key) not in (None, "", [], {}))
    scores["contract"] += round(12 * present / len(required_top))
    if spec.get("schema_version"):
        scores["contract"] += 2
    if isinstance(spec.get("goal"), str) and len(spec["goal"].strip()) >= 20:
        scores["contract"] += 3
    if spec.get("risk_class") in {"L0", "L1", "L2", "L3", "L4", "L5"}:
        scores["contract"] += 3
    if present < len(required_top):
        missing = [key for key in required_top if key not in spec or spec.get(key) in (None, "", [], {})]
        findings.append("contract: missing top-level blocks: " + ", ".join(missing))

    tools = _object(spec.get("tools"))
    gates = _object(spec.get("human_gate"))
    isolation = _object(spec.get("isolation"))
    forbidden = set(tools.get("forbidden_actions") or [])
    required_for = set(gates.get("required_for") or [])
    risk_class = spec.get("risk_class", "L0")
    risk_level = int(str(risk_class)[1]) if isinstance(risk_class, str) and risk_class[1:].isdigit() else 0
    if _covers_dangers(forbidden):
        scores["safety"] += 7
    else:
        findings.append("safety: forbidden_actions should cover deletion, secrets, posting, deploy and payments")
    if _covers_dangers(required_for):
        scores["safety"] += 7
    else:
        findings.append("safety: human_gate.required_for should cover dangerous actions")
    if isolation.get("mode") in REAL_ISOLATION:
        scores["safety"] += 3
    else:
        findings.append("safety: isolation.mode should be explicit")
    if risk_level < 3 or isolation.get("mode") in {"git_worktree", "temp_dir", "container", "profile_boundary", "read_only"}:
        scores["safety"] += 3
    else:
        findings.append("safety: L3+ loops need strong isolation")

    verification = _object(spec.get("verification"))
    deterministic = verification.get("deterministic_checks") or []
    review = verification.get("review_checks") or []
    dod = verification.get("definition_of_done") or []
    if _nonempty_list(deterministic):
        scores["verification"] += 8
    else:
        findings.append("verification: add deterministic checks, not only model/self-review")
    if _nonempty_list(review):
        scores["verification"] += 4
    if _nonempty_list(dod):
        scores["verification"] += 4
    if any(isinstance(x, dict) and x.get("pass_condition") for x in deterministic):
        scores["verification"] += 4
    else:
        findings.append("verification: deterministic checks should include pass_condition")

    receipt = _object(spec.get("receipt"))
    outputs = _object(spec.get("outputs"))
    state = _object(spec.get("state"))
    if receipt.get("required") is True and receipt.get("path"):
        scores["observability"] += 5
    else:
        findings.append("observability: require a receipt path")
    if _nonempty_list(outputs.get("artifacts")):
        scores["observability"] += 3
    if state.get("read_before_run") is True:
        scores["observability"] += 3
    if state.get("update_after_run") is not None:
        scores["observability"] += 2
    if state.get("location"):
        scores["observability"] += 2

    trigger = _object(spec.get("trigger"))
    allowed = set(tools.get("allowed") or [])
    if trigger.get("type") in HERMES_TRIGGERS:
        scores["hermes_fit"] += 4
    else:
        findings.append("hermes_fit: trigger should map to manual/cron/webhook/kanban/github_issue/file_change")
    if state.get("backend") in HERMES_STATE or state.get("backend") == "none":
        scores["hermes_fit"] += 4
    if allowed:
        scores["hermes_fit"] += 3
    else:
        findings.append("hermes_fit: list allowed Hermes tools/capabilities")
    if any(str(x).startswith(("read_", "search_", "write_", "terminal", "web_", "kanban", "github")) for x in allowed):
        scores["hermes_fit"] += 2
    if gates.get("approval_format"):
        scores["hermes_fit"] += 2

    stop = _object(spec.get("stop_conditions"))
    if isinstance(stop.get("max_iterations"), int) and stop["max_iterations"] >= 1:
        scores["operability"] += 2
    else:
        findings.append("operability: max_iterations is required")
    if isinstance(stop.get("max_runtime_minutes"), int) and stop["max_runtime_minutes"] >= 1:
        scores["operability"] += 2
    if stop.get("success_signal"):
        scores["operability"] += 2
    if stop.get("failure_policy"):
        scores["operability"] += 2
    if stop.get("stop_on_repeated_error") is not None:
        scores["operability"] += 2

    for key, max_score in WEIGHTS.items():
        scores[key] = min(scores[key], max_score)
    total = sum(scores.values())
    verdict = "ready" if total >= 85 and not any(f.startswith("safety:") for f in findings) else "needs_work" if total >= 60 else "not_loop_engineered"
    return {"score": total, "max_score": 100, "verdict": verdict, "category_scores": scores, "findings": findings}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    results = []
    for path in args.paths:
        try:
            result = score_spec(load_yaml(path))
        except Exception as exc:  # pragma: no cover - defensive CLI edge
            result = {"score": 0, "max_score": 100, "verdict": "error", "category_scores": {}, "findings": [str(exc)]}
        result = {"path": path, **result}
        results.append(result)
    if args.json:
        print(json.dumps({"results": results}, ensure_ascii=False, indent=2))
    else:
        for result in results:
            print(f"{result['score']:3}/100 {result['verdict']:20} {result['path']}")
            for finding in result["findings"]:
                print(f"  - {finding}")
    return 0 if all(r["score"] >= 60 for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
