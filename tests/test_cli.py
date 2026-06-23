from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_cli_validate_and_score():
    validate = subprocess.run(
        [sys.executable, "-m", "hermes_loop.cli", "validate", "examples/daily-briefing-loop/loop-spec.yaml"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert validate.returncode == 0, validate.stdout + validate.stderr
    score = subprocess.run(
        [sys.executable, "-m", "hermes_loop.cli", "score", "examples/daily-briefing-loop/loop-spec.yaml"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert score.returncode == 0, score.stdout + score.stderr
    assert "ready" in score.stdout


def test_cli_dry_run(tmp_path):
    out = tmp_path / "run"
    r = subprocess.run(
        [
            sys.executable,
            "-m",
            "hermes_loop.cli",
            "dry-run",
            "examples/daily-briefing-loop/loop-spec.yaml",
            "--out",
            str(out),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert (out / "run-record.yaml").exists()
    assert (out / "receipt.md").exists()


def test_cli_init_refuses_overwrite(tmp_path):
    target = tmp_path / "loop-spec.yaml"
    first = subprocess.run([sys.executable, "-m", "hermes_loop.cli", "init", str(target)], cwd=ROOT, text=True, capture_output=True)
    second = subprocess.run([sys.executable, "-m", "hermes_loop.cli", "init", str(target)], cwd=ROOT, text=True, capture_output=True)
    assert first.returncode == 0
    assert second.returncode != 0
