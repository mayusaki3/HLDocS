"""Tests for generator orchestration."""

from __future__ import annotations

import json
from pathlib import Path

from hldocs_html.generator import generate

VALID_MARKDOWN = """<!--
HLDocS:LLM-MANAGED
doc_id: doc-test-001
lang: ja-JP
canonical_title: テスト仕様
document_type: spec
canonical_document: true
-->

# テスト仕様

## 目的

本文です。
"""


def _write_valid_markdown(input_root: Path) -> None:
    source = input_root / "仕様" / "00_共通"
    source.mkdir(parents=True)
    (source / "01_テスト仕様.md").write_text(VALID_MARKDOWN, encoding="utf-8")


# HTML-POC-UT-008
def test_generate_outputs_index_overview_reference_and_manifest(tmp_path: Path) -> None:
    input_root = tmp_path / "docs" / "ja-JP"
    _write_valid_markdown(input_root)

    output_root = input_root / "HTMLドキュメント"

    generate(input_root, output_root, ["overview", "reference"])

    assert (output_root / "index.html").exists()
    assert (output_root / "overview" / "index.html").exists()
    assert list((output_root / "reference").glob("*.html"))
    assert (output_root / "manifest" / "site-manifest.json").exists()


# HTML-POC-UT-009
def test_manifest_contains_required_page_fields(tmp_path: Path) -> None:
    input_root = tmp_path / "docs" / "ja-JP"
    _write_valid_markdown(input_root)

    output_root = input_root / "HTMLドキュメント"
    generate(input_root, output_root, ["overview", "reference"])

    manifest = json.loads((output_root / "manifest" / "site-manifest.json").read_text(encoding="utf-8"))

    assert manifest["profile"] == ["overview", "reference"]
    assert manifest["pages"]


# HTML-POC-UT-010
def test_generated_paths_do_not_contain_spaces(tmp_path: Path) -> None:
    input_root = tmp_path / "docs" / "ja-JP"
    _write_valid_markdown(input_root)

    output_root = input_root / "HTMLドキュメント"
    generate(input_root, output_root, ["overview", "reference"])

    assert [path for path in output_root.rglob("*") if " " in path.name] == []


# HTML-POC-UT-011
def test_not_generated_is_displayed_in_index(tmp_path: Path) -> None:
    input_root = tmp_path / "docs" / "ja-JP"
    _write_valid_markdown(input_root)

    output_root = input_root / "HTMLドキュメント"
    generate(input_root, output_root, ["overview", "reference"])

    index_html = (output_root / "index.html").read_text(encoding="utf-8")

    assert "Not generated" in index_html
    assert "traceability" in index_html
    assert "test-report" in index_html


# HTML-POC-UT-012
def test_manifest_link_targets_only_reference_existing_pages(tmp_path: Path) -> None:
    input_root = tmp_path / "docs" / "ja-JP"
    _write_valid_markdown(input_root)

    output_root = input_root / "HTMLドキュメント"
    generate(input_root, output_root, ["overview", "reference"])

    manifest = json.loads((output_root / "manifest" / "site-manifest.json").read_text(encoding="utf-8"))

    page_ids = {page["page_id"] for page in manifest["pages"]}

    for page in manifest["pages"]:
        assert set(page["link_targets"]).issubset(page_ids)
