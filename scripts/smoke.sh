#!/usr/bin/env bash
set -euo pipefail

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

good_specs=(
  examples/coding-fix-loop/loop-spec.yaml
  examples/daily-briefing-loop/loop-spec.yaml
  examples/diagnostic-loop/loop-spec.yaml
  examples/hermes-cron-daily-briefing-loop/loop-spec.yaml
  examples/repo-maintenance-loop/loop-spec.yaml
  examples/research-watchlist-loop/loop-spec.yaml
)

python scripts/validate_loop_spec.py "${good_specs[@]}"
python scripts/validate_loop_spec.py examples/bad-cron-repo-editor/loop-spec.yaml && { echo 'bad example unexpectedly passed'; exit 1; } || true
python scripts/evaluate_loop_spec.py examples/emulation-prompt-only.yaml || true
python scripts/evaluate_loop_spec.py "${good_specs[@]}"
python scripts/dry_run_loop.py examples/daily-briefing-loop/loop-spec.yaml --run-record-out "$tmp/daily-run-record.yaml" --receipt-out "$tmp/daily-receipt.md"
python scripts/render_loop_receipt.py examples/daily-briefing-loop/run-record.yaml > "$tmp/daily-briefing.receipt.md"
python scripts/scan_loop_privacy.py .
pytest -q
