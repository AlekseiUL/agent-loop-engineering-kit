from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from importlib import resources

from hermes_loop import dry_run_loop, evaluate_loop_spec, render_loop_receipt, scan_loop_privacy, validate_loop_spec


def resource_path(*parts: str):
    return resources.files("hermes_loop").joinpath("resources", *parts)


def cmd_validate(args: argparse.Namespace) -> int:
    return validate_loop_spec.main([*args.paths, *( ["--json"] if args.json else [] )])


def cmd_score(args: argparse.Namespace) -> int:
    return evaluate_loop_spec.main([*args.paths, *( ["--json"] if args.json else [] )])


def cmd_dry_run(args: argparse.Namespace) -> int:
    out = Path(args.out)
    return dry_run_loop.main(
        [
            args.loop_spec,
            "--run-record-out",
            str(out / "run-record.yaml"),
            "--receipt-out",
            str(out / "receipt.md"),
            "--min-score",
            str(args.min_score),
            *( ["--json"] if args.json else [] ),
        ]
    )


def cmd_render_receipt(args: argparse.Namespace) -> int:
    return render_loop_receipt.main([args.run_record])


def cmd_privacy_scan(args: argparse.Namespace) -> int:
    return scan_loop_privacy.main([args.root, *( ["--json"] if args.json else [] )])


def cmd_smoke(_: argparse.Namespace) -> int:
    cwd = Path.cwd()
    source_smoke = cwd / "scripts" / "smoke.sh"
    if source_smoke.exists():
        return subprocess.call(["bash", str(source_smoke)], cwd=cwd)
    examples = sorted(str(p) for p in (cwd / "examples").glob("*/loop-spec.yaml"))
    if not examples:
        print("smoke requires a repository with examples/*/loop-spec.yaml", file=sys.stderr)
        return 1
    rc = validate_loop_spec.main([*examples])
    rc = evaluate_loop_spec.main([*examples]) or rc
    rc = scan_loop_privacy.main([str(cwd)]) or rc
    if (cwd / "tests").exists():
        rc = subprocess.call([sys.executable, "-m", "pytest", "-q"], cwd=cwd) or rc
    return rc


def cmd_init(args: argparse.Namespace) -> int:
    target = Path(args.path)
    if target.exists() and not args.force:
        print(f"refusing to overwrite existing file: {target}", file=sys.stderr)
        return 1
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(resource_path("templates", "loop-spec.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    print(f"created {target}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hermes-loop", description="Design, validate and dry-run safe Hermes Agent loops.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("validate", help="Validate loop spec schema and safety rules")
    p.add_argument("paths", nargs="+")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("score", aliases=["evaluate"], help="Score loop-engineering usefulness")
    p.add_argument("paths", nargs="+")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_score)

    p = sub.add_parser("dry-run", help="Create a safe contract dry-run record and receipt")
    p.add_argument("loop_spec")
    p.add_argument("--out", required=True, help="Output directory for run-record.yaml and receipt.md")
    p.add_argument("--min-score", type=int, default=85)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_dry_run)

    p = sub.add_parser("render-receipt", help="Render a validated run-record YAML as Markdown")
    p.add_argument("run_record")
    p.set_defaults(func=cmd_render_receipt)

    p = sub.add_parser("privacy-scan", help="Scan specs/docs/examples for common secrets and private paths")
    p.add_argument("root", nargs="?", default=".")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_privacy_scan)

    p = sub.add_parser("smoke", help="Run repository smoke checks")
    p.set_defaults(func=cmd_smoke)

    p = sub.add_parser("init", help="Copy the loop spec template to a target path")
    p.add_argument("path")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_init)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
