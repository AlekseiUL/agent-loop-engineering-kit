from pathlib import Path
import subprocess
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]


def good_specs():
    return sorted(str(p) for p in (ROOT / "examples").glob("*/loop-spec.yaml") if "bad-" not in p.parts[-2])


def test_all_examples_validate():
    r = subprocess.run([sys.executable, "scripts/validate_loop_spec.py", *good_specs()], cwd=ROOT, text=True, capture_output=True)
    assert r.returncode == 0, r.stdout + r.stderr


def test_bad_cron_repo_editor_is_blocked():
    bad = ROOT / "examples/bad-cron-repo-editor/loop-spec.yaml"
    r = subprocess.run([sys.executable, "scripts/validate_loop_spec.py", str(bad)], cwd=ROOT, text=True, capture_output=True)
    output = r.stdout + r.stderr
    assert r.returncode != 0
    assert "cron-triggered L3+ blocked" in output
    assert "L3+ requires deterministic verification" in output


def test_invalid_missing_stop_condition_fails(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text('schema_version: "1.0"\nname: bad\ngoal: bad\nrisk_class: L1\ntrigger: {type: manual}\ninputs: {required: [x]}\nstate: {backend: file, location: state.json, read_before_run: true}\ntools: {allowed: [read_files], forbidden_actions: [delete_files, access_secrets, public_posting, production_deploy, payments]}\nisolation: {mode: read_only}\nverification: {deterministic_checks: [], review_checks: []}\nhuman_gate: {required_for: [deletion, secrets, public_posting, production_deploy, payments], approval_format: APPROVE}\noutputs: {artifacts: [report.md]}\nreceipt: {required: true, path: receipt.md}\n')
    r = subprocess.run([sys.executable, "scripts/validate_loop_spec.py", str(bad)], cwd=ROOT, text=True, capture_output=True)
    assert r.returncode != 0 and "stop_conditions" in (r.stdout + r.stderr)


def test_human_gate_must_cover_all_dangerous_actions(tmp_path):
    weak = tmp_path / "weak-gate.yaml"
    weak.write_text('schema_version: "1.0"\nname: weak\ngoal: weak safety gate example\nrisk_class: L2\ntrigger: {type: manual}\ninputs: {required: [x]}\nstate: {backend: file, location: state.json, read_before_run: true}\ntools: {allowed: [read_files], forbidden_actions: [delete_files, access_secrets, public_posting, production_deploy, payments]}\nisolation: {mode: read_only}\nverification: {deterministic_checks: [{name: check, method: command, pass_condition: pass}], review_checks: []}\nstop_conditions: {max_iterations: 1, max_runtime_minutes: 5, success_signal: done, failure_policy: stop}\nhuman_gate: {required_for: [deletion], approval_format: APPROVE}\noutputs: {artifacts: [report.md]}\nreceipt: {required: true, path: receipt.md}\n')
    r = subprocess.run([sys.executable, "scripts/validate_loop_spec.py", str(weak)], cwd=ROOT, text=True, capture_output=True)
    output = r.stdout + r.stderr
    assert r.returncode != 0
    assert "human gates missing dangerous actions" in output
    assert "secrets" in output and "public_posting" in output


def test_deterministic_checks_must_be_structured(tmp_path):
    spec = yaml.safe_load((ROOT / "examples/coding-fix-loop/loop-spec.yaml").read_text(encoding="utf-8"))
    spec["verification"]["deterministic_checks"] = ["pytest -q"]
    path = tmp_path / "bad-verification.yaml"
    path.write_text(yaml.safe_dump(spec), encoding="utf-8")
    r = subprocess.run([sys.executable, "scripts/validate_loop_spec.py", str(path)], cwd=ROOT, text=True, capture_output=True)
    output = r.stdout + r.stderr
    assert r.returncode != 0
    assert "pass_condition" in output or "is not of type 'object'" in output


def test_max_iterations_above_three_accepts_rationale(tmp_path):
    spec = yaml.safe_load((ROOT / "examples/daily-briefing-loop/loop-spec.yaml").read_text(encoding="utf-8"))
    spec["stop_conditions"]["max_iterations"] = 4
    spec["stop_conditions"]["rationale"] = "Needed to retry transient source failures."
    path = tmp_path / "rationale.yaml"
    path.write_text(yaml.safe_dump(spec), encoding="utf-8")
    r = subprocess.run([sys.executable, "scripts/validate_loop_spec.py", str(path)], cwd=ROOT, text=True, capture_output=True)
    assert r.returncode == 0, r.stdout + r.stderr
