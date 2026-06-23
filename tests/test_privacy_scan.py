from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_privacy_scan_passes_repo():
    r = subprocess.run([sys.executable, "scripts/scan_loop_privacy.py", "."], cwd=ROOT, text=True, capture_output=True)
    assert r.returncode == 0, r.stdout + r.stderr


def test_privacy_scan_catches_token(tmp_path):
    token = "1234567890:" + "ABCDEFGHIJKLMNOPQRSTUVWXYZabc"
    (tmp_path / "bad.md").write_text(token)
    r = subprocess.run([sys.executable, str(ROOT / "scripts/scan_loop_privacy.py"), str(tmp_path)], text=True, capture_output=True)
    assert r.returncode != 0 and "telegram_token" in r.stdout


def test_privacy_scan_catches_yaml_secret_assignment(tmp_path):
    key = "sk-" + "A" * 24
    (tmp_path / "bad.yaml").write_text(f"api_key: {key}\n", encoding="utf-8")
    r = subprocess.run([sys.executable, str(ROOT / "scripts/scan_loop_privacy.py"), str(tmp_path)], text=True, capture_output=True)
    assert r.returncode != 0
    assert "api_key_assignment" in r.stdout or "openai_key" in r.stdout


def test_privacy_scan_catches_common_provider_tokens(tmp_path):
    github = "ghp_" + "A" * 36
    aws = "AKIA" + "1" * 16
    slack = "xoxb-" + "1" * 12 + "-" + "a" * 24
    (tmp_path / "bad.txt").write_text(f"{github}\n{aws}\n{slack}\n", encoding="utf-8")
    r = subprocess.run([sys.executable, str(ROOT / "scripts/scan_loop_privacy.py"), str(tmp_path)], text=True, capture_output=True)
    assert r.returncode != 0
    assert "github_token" in r.stdout and "aws_access_key" in r.stdout and "slack_token" in r.stdout
