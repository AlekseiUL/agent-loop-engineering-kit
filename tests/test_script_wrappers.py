from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_MODULES = {
    "validate_loop_spec.py": "validate_loop_spec",
    "evaluate_loop_spec.py": "evaluate_loop_spec",
    "dry_run_loop.py": "dry_run_loop",
    "render_loop_receipt.py": "render_loop_receipt",
    "scan_loop_privacy.py": "scan_loop_privacy",
    "audit_report.py": "audit_report",
}


def test_script_entrypoints_are_thin_package_wrappers():
    for script_name, module_name in SCRIPT_MODULES.items():
        text = (ROOT / "scripts" / script_name).read_text(encoding="utf-8")
        assert f"hermes_loop.{module_name}" in text
        assert "raise SystemExit(main())" in text
        assert len(text.splitlines()) <= 20
