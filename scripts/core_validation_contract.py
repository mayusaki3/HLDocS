#!/usr/bin/env python3
"""HLDocS Core validation contract checker (STATIC only).

This tool validates fixture metadata and case coverage. It does not execute
the HLDocS Core, simulate its behavior, or award runtime PASS.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

CASE_IDS = tuple([f"WS-{i:02d}" for i in range(1, 5)] + [f"FC-{i:02d}" for i in range(1, 11)])
REQUIRED = ("case_id", "target_sha", "mode", "initial_state", "preconditions", "stimulus", "expected")
MODES = {"STATIC", "SIMULATED", "EXECUTED"}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def validate_fixture(obj: object, expected_case: str | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(obj, dict):
        return ["fixture must be a JSON object"]
    for key in REQUIRED:
        if key not in obj:
            errors.append(f"missing: {key}")
    case_id = obj.get("case_id")
    if case_id not in CASE_IDS:
        errors.append(f"unknown case_id: {case_id!r}")
    if expected_case is not None and case_id != expected_case:
        errors.append(f"case_id mismatch: {case_id!r} != {expected_case!r}")
    sha = obj.get("target_sha")
    if not isinstance(sha, str) or SHA_RE.fullmatch(sha) is None:
        errors.append("target_sha must be a fixed 40-character lowercase commit SHA")
    if obj.get("mode") not in MODES:
        errors.append("mode must be STATIC, SIMULATED, or EXECUTED")
    if not isinstance(obj.get("initial_state"), str) or not obj.get("initial_state"):
        errors.append("initial_state must be a nonempty fixture reference")
    if not isinstance(obj.get("preconditions"), list):
        errors.append("preconditions must be a list")
    for key in ("stimulus", "expected"):
        if not isinstance(obj.get(key), dict) or not obj.get(key):
            errors.append(f"{key} must be a nonempty object")
    return errors


def check_case_catalog(text: str) -> list[str]:
    ids = re.findall(r"^\|\s*((?:WS|FC)-\d{2})\s*\|", text, re.MULTILINE)
    errors: list[str] = []
    for case in CASE_IDS:
        if ids.count(case) != 1:
            errors.append(f"{case}: expected once, found {ids.count(case)}")
    for case in ids:
        if case not in CASE_IDS:
            errors.append(f"unexpected case: {case}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=pathlib.Path, required=True)
    parser.add_argument("--fixtures", type=pathlib.Path, help="optional directory of JSON fixture definitions")
    args = parser.parse_args()
    errors: list[str] = []
    try:
        catalog = args.catalog.read_text(encoding="utf-8")
        errors.extend(check_case_catalog(catalog))
    except OSError as exc:
        errors.append(f"catalog: {exc}")
    checked = 0
    if args.fixtures is not None:
        if not args.fixtures.is_dir():
            errors.append(f"fixture directory missing: {args.fixtures}")
        else:
            seen: set[str] = set()
            for path in sorted(args.fixtures.glob("*.json")):
                checked += 1
                try:
                    obj = json.loads(path.read_text(encoding="utf-8"))
                    problems = validate_fixture(obj)
                    if isinstance(obj, dict) and obj.get("case_id") in seen:
                        problems.append("duplicate case_id across fixtures")
                    if isinstance(obj, dict) and isinstance(obj.get("case_id"), str):
                        seen.add(obj["case_id"])
                    errors.extend(f"{path.name}: {problem}" for problem in problems)
                except (OSError, json.JSONDecodeError) as exc:
                    errors.append(f"{path.name}: {exc}")
    result = {
        "tool": "core_validation_contract",
        "validation_mode": "STATIC",
        "runtime_executed": False,
        "core_normality_verdict": "UNDETERMINED",
        "catalog_cases_expected": len(CASE_IDS),
        "fixtures_checked": checked,
        "contract_check": "FAIL" if errors else "PASS",
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
