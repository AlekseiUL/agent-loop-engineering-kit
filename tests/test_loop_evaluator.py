from pathlib import Path
import subprocess
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_evaluator_scores_real_examples_high_enough():
    specs = sorted(str(p) for p in (ROOT / "examples").glob("*/loop-spec.yaml") if not p.as_posix().endswith("bad-cron-repo-editor/loop-spec.yaml"))
    r = subprocess.run(
        [sys.executable, "scripts/evaluate_loop_spec.py", *specs, "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert '"score"' in r.stdout


def test_evaluator_shows_prompt_only_is_not_loop_engineered(tmp_path):
    loose = tmp_path / "loose.yaml"
    loose.write_text('goal: "make a daily briefing"\n', encoding="utf-8")
    r = subprocess.run(
        [sys.executable, "scripts/evaluate_loop_spec.py", str(loose)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert r.returncode != 0
    assert "not_loop_engineered" in r.stdout
    assert "missing top-level blocks" in r.stdout


def test_evaluator_accepts_human_gate_aliases(tmp_path):
    spec = yaml.safe_load((ROOT / "examples/daily-briefing-loop/loop-spec.yaml").read_text(encoding="utf-8"))
    spec["human_gate"]["required_for"] = [
        "delete_files",
        "access_secrets",
        "send_messages",
        "deploy_production",
        "billing",
    ]
    path = tmp_path / "alias-gate.yaml"
    path.write_text(yaml.safe_dump(spec), encoding="utf-8")
    r = subprocess.run(
        [sys.executable, "scripts/evaluate_loop_spec.py", str(path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ready" in r.stdout
    assert "human_gate.required_for should cover dangerous actions" not in r.stdout
