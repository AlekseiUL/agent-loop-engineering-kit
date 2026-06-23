from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_dry_run_loop_creates_valid_run_record_and_receipt(tmp_path):
    run_record = tmp_path / "run-record.yaml"
    receipt = tmp_path / "receipt.md"
    r = subprocess.run(
        [
            sys.executable,
            "scripts/dry_run_loop.py",
            "examples/daily-briefing-loop/loop-spec.yaml",
            "--run-record-out",
            str(run_record),
            "--receipt-out",
            str(receipt),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert run_record.exists() and receipt.exists()
    rendered = subprocess.run(
        [sys.executable, "scripts/render_loop_receipt.py", str(run_record)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert rendered.returncode == 0, rendered.stdout + rendered.stderr
    assert "dry_run_contract_verified_no_task_execution" in receipt.read_text(encoding="utf-8")


def test_dry_run_loop_rejects_prompt_only(tmp_path):
    r = subprocess.run(
        [
            sys.executable,
            "scripts/dry_run_loop.py",
            "examples/emulation-prompt-only.yaml",
            "--run-record-out",
            str(tmp_path / "run.yaml"),
            "--receipt-out",
            str(tmp_path / "receipt.md"),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert r.returncode != 0
    assert "failed" in r.stderr.lower() or "required" in r.stderr.lower()
