from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_receipt_renderer_outputs_markdown():
    r = subprocess.run(
        [sys.executable, "scripts/render_loop_receipt.py", "examples/daily-briefing-loop/run-record.yaml"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert r.returncode == 0
    assert "# Loop Run Receipt" in r.stdout and "daily-briefing-loop" in r.stdout and "dry_run_example_complete" in r.stdout


def test_receipt_renderer_rejects_missing_required_fields(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("loop_name: x\n", encoding="utf-8")
    r = subprocess.run(
        [sys.executable, "scripts/render_loop_receipt.py", str(bad)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert r.returncode != 0
    assert "invalid run record" in r.stderr and "required" in r.stderr
