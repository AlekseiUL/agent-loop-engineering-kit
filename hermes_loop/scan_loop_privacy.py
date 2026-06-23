#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

PATTERNS = {
    "telegram_token": re.compile(r"\b\d{8,12}:[A-Za-z0-9_-]{25,}\b"),
    "api_key_assignment": re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./:+-]{12,}"),
    "private_key": re.compile(r"BEGIN (RSA|OPENSSH|PRIVATE) KEY"),
    "github_token": re.compile(r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{30,}\b|\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    "openai_key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "slack_token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "mac_private_path": re.compile(r"/Users/[A-Za-z0-9._-]+/(Desktop|Documents|Downloads)/"),
    "linux_home_path": re.compile(r"/home/[A-Za-z0-9._-]+/"),
}
SUFFIX = {".md", ".yaml", ".yml", ".json", ".py", ".toml", ".txt"}
IGNORE_PARTS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache"}


def scan(root: str) -> list[dict[str, object]]:
    findings = []
    root_path = Path(root).resolve()
    for path in root_path.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SUFFIX:
            continue
        rel = path.relative_to(root_path)
        if any(part in IGNORE_PARTS for part in rel.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for name, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                findings.append(
                    {
                        "file": rel.as_posix(),
                        "type": name,
                        "line": text.count("\n", 0, match.start()) + 1,
                        "match": match.group(0)[:80],
                    }
                )
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    findings = scan(args.root)
    if args.json:
        print(json.dumps({"ok": not findings, "findings": findings}, ensure_ascii=False, indent=2))
    else:
        print("PASS privacy scan" if not findings else "FAIL privacy scan")
        for item in findings:
            print(f"{item['file']}:{item['line']} {item['type']} {item['match']}")
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
