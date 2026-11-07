#!/usr/bin/env python3
"""Regression tests for the STATIC-only Core validation contract checker."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "core_validation_contract.py"
CASES = [f"WS-{n:02d}" for n in range(1, 5)] + [f"FC-{n:02d}" for n in range(1, 11)]
SHA = "a" * 40


def load_checker():
    """Import checker functions without executing its CLI entry point."""
    spec = importlib.util.spec_from_file_location("core_checker_under_test", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CHECKER = load_checker()


def fixture(case_id: str) -> dict:
    return {
        "case_id": case_id,
        "target_sha": SHA,
        "mode": "STATIC",
        "initial_state": "isolated-fixture",
        "preconditions": [],
        "stimulus": {"operation": "contract-check-only"},
        "expected": {"decision": "deny"},
        "fixture_id": f"core-validation-{case_id.lower()}",
        "canonical_snapshot": {"status": "UNRESOLVED", "reason": "not configured"},
        "initial_context": {"status": "UNRESOLVED", "reason": "not configured"},
        "provider_stub": {"status": "UNRESOLVED", "reason": "not configured"},
        "restriction_stub": {"status": "UNRESOLVED", "reason": "not configured"},
        "fault_injection": {"status": "UNRESOLVED", "reason": "not configured"},
        "expected_invariants": ["do_not_execute_core"],
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
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7a13bc90c48f2a7183d1e602b6e9402c
        # @hldocs.label CV-CONTRACT-001
        status, result = self.run_checker(with_fixtures=False)
        self.assertEqual(status, 0)
        self.assertEqual(result["contract_check"], "PASS")
        self.assertFalse(result["sut_execution_ready"])
        self.assertFalse(result["runtime_executed"])
        self.assertEqual(result["core_normality_verdict"], "UNDETERMINED")

    def test_empty_fixture_directory_fails(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7a27023bc4b447aa83eca9f3b6fd6613
        # @hldocs.label CV-CONTRACT-002
        status, result = self.run_checker()
        self.assertEqual(status, 1)
        self.assertEqual(result["contract_check"], "FAIL")
        self.assertEqual(len([e for e in result["errors"] if e.startswith("missing fixture")]), 14)

    def test_all_fourteen_valid_fixtures_pass_contract_only(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7a3a47e6c4d964e384076de4b7118bfa
        # @hldocs.label CV-CONTRACT-003
        for case in CASES:
            self.add_fixture(case)
        status, result = self.run_checker()
        self.assertEqual(status, 0)
        self.assertEqual(result["fixtures_checked"], 14)
        self.assertEqual(result["contract_check"], "PASS")
        self.assertFalse(result["runtime_executed"])
        self.assertEqual(result["core_normality_verdict"], "UNDETERMINED")

    def test_one_missing_fixture_fails(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7a4d8d91c4fe821c842231d5b725b1e1
        # @hldocs.label CV-CONTRACT-004
        for case in CASES[:-1]:
            self.add_fixture(case)
        status, result = self.run_checker()
        self.assertEqual(status, 1)
        self.assertTrue(any("FC-10" in e for e in result["errors"]))

    def test_duplicate_fixture_fails(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7a60d33cc5239f55843cf5c6b739d7c8
        # @hldocs.label CV-CONTRACT-005
        for case in CASES:
            self.add_fixture(case)
        self.add_fixture(CASES[0], "duplicate")
        status, result = self.run_checker()
        self.assertEqual(status, 1)
        self.assertTrue(any("duplicate case_id" in e for e in result["errors"]))

    def test_invalid_sha_fails(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7a7418e7c548bc8e8457b9b7b74dfdaf
        # @hldocs.label CV-CONTRACT-006
        for case in CASES:
            self.add_fixture(case)
        bad = fixture(CASES[0])
        bad["target_sha"] = "develop"
        self.add_fixture(CASES[0], data=bad)
        status, result = self.run_checker()
        self.assertEqual(status, 1)
        self.assertTrue(any("target_sha" in e for e in result["errors"]))

    def test_missing_formal_field_fails(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7a9aa43dc592f700848d4199b776497d
        # @hldocs.label CV-CONTRACT-008
        # CV-CONTRACT-008: A formal field required by the SUT contract must exist.
        for case in CASES:
            self.add_fixture(case)
        bad = fixture(CASES[0])
        del bad["canonical_snapshot"]
        self.add_fixture(CASES[0], data=bad)
        status, result = self.run_checker()
        self.assertEqual(status, 1)
        self.assertTrue(any("canonical_snapshot" in e for e in result["errors"]))

    def test_unresolved_boundary_requires_reason(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7aade9e8c5b8143984a8058ab78a6f64
        # @hldocs.label CV-CONTRACT-009
        # CV-CONTRACT-009: Unresolved injection points cannot omit rationale.
        for case in CASES:
            self.add_fixture(case)
        bad = fixture(CASES[0])
        bad["fault_injection"] = {"status": "UNRESOLVED"}
        self.add_fixture(CASES[0], data=bad)
        status, result = self.run_checker()
        self.assertEqual(status, 1)
        self.assertTrue(any("UNRESOLVED requires a reason" in e for e in result["errors"]))

    def test_empty_invariants_fails(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7ac12f93c5dd317284c2c97bb79e954b
        # @hldocs.label CV-CONTRACT-010
        # CV-CONTRACT-010: Expected invariants cannot be omitted.
        for case in CASES:
            self.add_fixture(case)
        bad = fixture(CASES[0])
        bad["expected_invariants"] = []
        self.add_fixture(CASES[0], data=bad)
        status, result = self.run_checker()
        self.assertEqual(status, 1)
        self.assertTrue(any("expected_invariants" in e for e in result["errors"]))

    def test_missing_catalog_case_fails(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7a875e92c56dd9c784727da8b7622396
        # @hldocs.label CV-CONTRACT-007
        self.catalog.write_text(
            "| ケース | 内容 |\n| --- | --- |\n"
            + "".join(f"| {case} | test |\n" for case in CASES[:-1]),
            encoding="utf-8",
        )
        status, result = self.run_checker(with_fixtures=False)
        self.assertEqual(status, 1)
        self.assertTrue(any("FC-10" in e for e in result["errors"]))

    def fill(self) -> None:
        """Create a complete valid fixture set for negative-case isolation."""
        for case in CASES:
            self.add_fixture(case)

    def reject(self, key: str, value: object, expected_error: str) -> None:
        """Check one malformed fixture field through the CLI."""
        self.fill()
        bad = fixture(CASES[0])
        bad[key] = value
        self.add_fixture(CASES[0], data=bad)
        status, result = self.run_checker()
        self.assertEqual(status, 1)
        self.assertEqual(result["contract_check"], "FAIL")
        self.assertTrue(any(expected_error in e for e in result["errors"]), result["errors"])

    def test_non_object_fixture_fails(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7ad4753ec6024eab84dd8d6cb7b2bb32
        # @hldocs.label CV-CONTRACT-011
        self.fill(); self.add_fixture(CASES[0], data=[])
        status, result = self.run_checker()
        self.assertEqual(status, 1)
        self.assertTrue(any("fixture must be a JSON object" in e for e in result["errors"]))

    def test_unknown_fixture_case_fails(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7ae7bae9c6276be484f8515db7c6e119
        # @hldocs.label CV-CONTRACT-012
        self.reject("case_id", "WS-99", "unknown case_id")

    def test_expected_case_mismatch_fails(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7afb0094c64c891d8513154eb7db0700
        # @hldocs.label CV-CONTRACT-013
        errors = CHECKER.validate_fixture(fixture("WS-01"), expected_case="FC-01")
        self.assertTrue(any("case_id mismatch" in e for e in errors))

    def test_invalid_fixture_id_fails(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7b0e463fc671a656852dd93fb7ef2ce7
        # @hldocs.label CV-CONTRACT-014
        for value in ("", 123):
            with self.subTest(value=value):
                self.reject("fixture_id", value, "fixture_id")

    def test_invalid_mode_fails(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7b218beac696c38f85489d30b80352ce
        # @hldocs.label CV-CONTRACT-015
        self.reject("mode", "INVALID", "mode must")

    def test_invalid_initial_state_fails(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7b34d195c6bbe0c885636121b81778b5
        # @hldocs.label CV-CONTRACT-016
        for value in ("", 123):
            with self.subTest(value=value):
                self.reject("initial_state", value, "initial_state")

    def test_invalid_preconditions_fails(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7b481740c6e0fe01857e2512b82b9e9c
        # @hldocs.label CV-CONTRACT-017
        self.reject("preconditions", {}, "preconditions")

    def test_invalid_stimulus_expected_fail(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7b5b5cebc7061b3a8598e903b83fc483
        # @hldocs.label CV-CONTRACT-018
        for key in ("stimulus", "expected"):
            for value in ({}, []):
                with self.subTest(key=key, value=value):
                    self.reject(key, value, key)

    def test_invalid_boundary_fields_fail(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7b6ea296c72b387385b3acf4b853ea6a
        # @hldocs.label CV-CONTRACT-019
        for key in CHECKER.BOUNDARY_FIELDS:
            for value in ({}, []):
                with self.subTest(key=key, value=value):
                    self.reject(key, value, key)

    def test_invalid_invariant_elements_fail(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7b81e841c75055ac85ce70e5b8681051
        # @hldocs.label CV-CONTRACT-020
        for value in ([""], [123]):
            with self.subTest(value=value):
                self.reject("expected_invariants", value, "expected_invariants")

    def test_unknown_catalog_case_fails(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7b952decc77572e585e934d6b87c3638
        # @hldocs.label CV-CONTRACT-021
        with self.catalog.open("a", encoding="utf-8") as stream:
            stream.write("| WS-99 | unexpected |\n")
        status, result = self.run_checker(with_fixtures=False)
        self.assertEqual(status, 1)
        self.assertTrue(any("unexpected case: WS-99" in e for e in result["errors"]))

    def test_duplicate_catalog_case_fails(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7ba87397c79a901e8603f8c7b8905c1f
        # @hldocs.label CV-CONTRACT-022
        with self.catalog.open("a", encoding="utf-8") as stream:
            stream.write("| WS-01 | duplicate |\n")
        status, result = self.run_checker(with_fixtures=False)
        self.assertEqual(status, 1)
        self.assertTrue(any("WS-01: expected once, found 2" in e for e in result["errors"]))

    def test_missing_catalog_file_fails(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7bbbb942c7bfad57861ebcb8b8a48206
        # @hldocs.label CV-CONTRACT-023
        self.catalog.unlink()
        status, result = self.run_checker(with_fixtures=False)
        self.assertEqual(status, 1)
        self.assertTrue(any(e.startswith("catalog:") for e in result["errors"]))

    def test_missing_fixture_directory_fails(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7bcefeedc7e4ca90863980a9b8b8a7ed
        # @hldocs.label CV-CONTRACT-024
        self.fixtures.rmdir()
        status, result = self.run_checker()
        self.assertEqual(status, 1)
        self.assertTrue(any("fixture directory missing:" in e for e in result["errors"]))

    def test_invalid_json_fails(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7be24498c809e7c98654449ab8cccdd4
        # @hldocs.label CV-CONTRACT-025
        self.fill()
        (self.fixtures / "WS-01.json").write_text("{not json", encoding="utf-8")
        status, result = self.run_checker()
        self.assertEqual(status, 1)
        self.assertTrue(any("WS-01.json:" in e for e in result["errors"]))

    def test_fixture_read_oserror_fails(self) -> None:
        # @hldocs.ref doc-20261107-021500Z-CVT1#sec_7bf58a43c82f0502866f088bb8e0f3bb
        # @hldocs.label CV-CONTRACT-026
        self.fill()
        original = pathlib.Path.read_text

        def injected_read(path: pathlib.Path, *args: object, **kwargs: object) -> str:
            """Inject an OSError for one fixture while leaving the catalog readable."""
            if path.name == "WS-01.json":
                raise OSError("injected fixture read error")
            return original(path, *args, **kwargs)

        output = io.StringIO()
        argv = ["core_validation_contract.py", "--catalog", str(self.catalog),
                "--fixtures", str(self.fixtures)]
        with mock.patch.object(sys, "argv", argv):
            with mock.patch.object(pathlib.Path, "read_text", injected_read):
                with contextlib.redirect_stdout(output):
                    status = CHECKER.main()
        result = json.loads(output.getvalue())
        self.assertEqual(status, 1)
        self.assertTrue(any("injected fixture read error" in e for e in result["errors"]))


if __name__ == "__main__":
    unittest.main()
