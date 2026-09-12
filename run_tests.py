#!/usr/bin/env python3
"""Language-neutral public test runner for decoder submissions."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [--cases-dir DIR] DECODER [DECODER_ARG ...]",
        description="Append CODE_TYPE and IMAGE_PATH to DECODER for every case.",
    )
    parser.add_argument("--cases-dir", type=Path, default=ROOT / "cases")
    parser.add_argument(
        "--type", action="append", dest="types",
        help="run only this CODE_TYPE (repeatable)",
    )
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("decoder", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.decoder and args.decoder[0] == "--":
        args.decoder = args.decoder[1:]
    if not args.decoder:
        parser.error("a decoder command is required")
    return args


def load_cases(root: Path) -> list[dict[str, str | Path]]:
    cases: list[dict[str, str | Path]] = []
    for image in sorted(root.glob("*/*/*.png")):
        expected_path = image.with_suffix(".txt")
        if not expected_path.is_file():
            raise ValueError(f"missing expected-output file: {expected_path}")
        relative = image.relative_to(root)
        cases.append({
            "name": relative.with_suffix("").as_posix(),
            "type": relative.parts[0],
            "image": image,
            "expected": expected_path.read_text(encoding="utf-8"),
        })
    if not cases:
        raise ValueError(f"no PNG fixtures found under {root}")
    return cases


def main() -> int:
    args = parse_args()
    cases_root = args.cases_dir.resolve()
    cases = load_cases(cases_root)
    if args.types:
        requested = set(args.types)
        cases = [case for case in cases if case["type"] in requested]
        if not cases:
            print("ERROR: no cases matched --type", file=sys.stderr)
            return 2
    passed = 0
    for case in cases:
        image = Path(case["image"])
        command = [*args.decoder, case["type"], str(image)]
        try:
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=args.timeout,
                check=False,
            )
        except subprocess.TimeoutExpired:
            print(f"FAIL {case['name']}: timed out after {args.timeout:g}s")
            continue
        except OSError as exc:
            print(f"ERROR: could not start decoder: {exc}", file=sys.stderr)
            return 2

        try:
            actual = result.stdout.decode("utf-8")
            stderr = result.stderr.decode("utf-8", errors="replace")
        except UnicodeDecodeError:
            print(f"FAIL {case['name']}: stdout is not UTF-8")
            continue
        expected = str(case["expected"])
        if result.returncode == 0 and actual == expected:
            print(f"PASS {case['name']}")
            passed += 1
        else:
            reason = f"exit {result.returncode}" if result.returncode else "wrong output"
            print(f"FAIL {case['name']}: {reason}")
            print(f"  expected: {expected!r}")
            print(f"  actual:   {actual!r}")
            if stderr:
                print(f"  stderr:   {stderr.rstrip()}")

    print(f"\n{passed}/{len(cases)} cases passed")
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    raise SystemExit(main())
