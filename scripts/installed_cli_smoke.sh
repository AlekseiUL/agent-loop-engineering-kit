#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
venv="${1:-$(mktemp -d)/venv}"
out="$(mktemp -d)"
trap 'rm -rf "$out"' EXIT

python3 -m venv "$venv"
"$venv/bin/python" -m pip install -q --upgrade pip
"$venv/bin/python" -m pip install -q "$repo"

cd "$repo"
"$venv/bin/hermes-loop" --help >/dev/null
"$venv/bin/hermes-loop" init "$out/loop-spec.yaml"
"$venv/bin/hermes-loop" validate examples/daily-briefing-loop/loop-spec.yaml --json >/dev/null
"$venv/bin/hermes-loop" score examples/daily-briefing-loop/loop-spec.yaml --json >/dev/null
"$venv/bin/hermes-loop" dry-run examples/daily-briefing-loop/loop-spec.yaml --out "$out/dry-run" --json >/dev/null
"$venv/bin/hermes-loop" render-receipt examples/daily-briefing-loop/run-record.yaml >/dev/null
"$venv/bin/hermes-loop" privacy-scan . --json >/dev/null

echo "PASS installed CLI smoke"
