#!/usr/bin/env python3
"""Regression tests for the STATIC-only Core validation contract checker."""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "core_validation_contract.py"
CASES = [f"WS-{n:02d}" for n in range(1, 5)] + [f"FC-{n:02d}" for n in range(1, 11)]
SHA = "a" * 40


def fixture(case_id: str) -> dict:
    return {
        "case_id": case_id,
        "target_sha": SHA,
        "mode": "STATIC",
        "initial_state": "isolated-fixture",
        "preconditions": [],
        "stimulus": {"operation": "contract-check-only"},
        "expected": {"decision": "deny"},
    }


class ContractCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = pathlib.Path(self.tmp.name)
        self.catalog = self.base / "catalog.md"
        self.fixtures = self.base / "fixtures"
        self.fixtures.mkdir()
        self.catalog.write_text(
            "| ケース | 内容 |\n| --- | --- |\n"
            + "".join(f"| {case} | test |\n" for case in CASES),
            encoding="utf-8",
        )

    def run_checker(self, *, with_fixtures: bool = True) -> tuple[int, dict]:
        command = [sys.executable, str(SCRIPT), "--catalog", str(self.catalog)]
        if with_fixtures:
            command.extend(["--fixtures", str(self.fixtures)])
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertTrue(result.stdout, result.stderr)
        return result.returncode, json.loads(result.stdout)

    def add_fixture(self, case: str, name: str | None = None, data: dict | None = None) -> None:
        (self.fixtures / (name or case) ).with_suffix(".json").write_text(
            json.dumps(fixture(case) if data is None else data), encoding="utf-8"
        )

    def test_catalog_only_is_static_pass_not_core_pass(self) -> None:
        status, result = self.run_checker(with_fixtures=False)
        self.assertEqual(status, 0)
        self.assertEqual(result["contract_check"], "PASS")
        self.assertFalse(result["runtime_executed"])
        self.assertEqual(result["core_normality_verdict"], "UNDETERMINED")

    def test_empty_fixture_directory_fails(self) -> None:
        status, result = self.run_checker()
        self.assertEqual(status, 1)
        self.assertEqual(result["contract_check"], "FAIL")
        self.assertEqual(len([e for e in result["errors"] if e.startswith("missing fixture")]), 14)

    def test_all_fourteen_valid_fixtures_pass_contract_only(self) -> None:
        for case in CASES:
            self.add_fixture(case)
        status, result = self.run_checker()
        self.assertEqual(status, 0)
        self.assertEqual(result["fixtures_checked"], 14)
        self.assertEqual(result["contract_check"], "PASS")
        self.assertFalse(result["runtime_executed"])
        self.assertEqual(result["core_normality_verdict"], "UNDETERMINED")

    def test_one_missing_fixture_fails(self) -> None:
        for case in CASES[:-1]:
            self.add_fixture(case)
        status, result = self.run_checker()
        self.assertEqual(status, 1)
        self.assertTrue(any("FC-10" in e for e in result["errors"]))

    def test_duplicate_fixture_fails(self) -> None:
        for case in CASES:
            self.add_fixture(case)
        self.add_fixture(CASES[0], "duplicate")
        status, result = self.run_checker()
        self.assertEqual(status, 1)
        self.assertTrue(any("duplicate case_id" in e for e in result["errors"]))

    def test_invalid_sha_fails(self) -> None:
        for case in CASES:
            self.add_fixture(case)
        bad = fixture(CASES[0])
        bad["target_sha"] = "develop"
        self.add_fixture(CASES[0], data=bad)
        status, result = self.run_checker()
        self.assertEqual(status, 1)
        self.assertTrue(any("target_sha" in e for e in result["errors"]))

    def test_missing_catalog_case_fails(self) -> None:
        self.catalog.write_text(
            "| ケース | 内容 |\n| --- | --- |\n"
            + "".join(f"| {case} | test |\n" for case in CASES[:-1]),
            encoding="utf-8",
        )
        status, result = self.run_checker(with_fixtures=False)
        self.assertEqual(status, 1)
        self.assertTrue(any("FC-10" in e for e in result["errors"]))


if __name__ == "__main__":
    unittest.main()
