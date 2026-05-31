"""Tests for markdown_loader."""

from __future__ import annotations

from pathlib import Path

from hldocs_html import markdown_loader

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

VALID_MARKDOWN_WITH_SEC_ID = """<!--
HLDocS:LLM-MANAGED
doc_id: doc-test-002
lang: ja-JP
canonical_title: sec_id テスト仕様
document_type: spec
canonical_document: true
-->

# sec_id テスト仕様

本文 sec_abc123 を含みます。
"""


# HTML-POC-UT-001
def test_parse_llm_managed_block_extracts_required_metadata() -> None:
    metadata = markdown_loader.parse_llm_managed_block(VALID_MARKDOWN)

    assert metadata is not None
    assert metadata["doc_id"] == "doc-test-001"
    assert metadata["lang"] == "ja-JP"
    assert metadata["canonical_title"] == "テスト仕様"
    assert metadata["document_type"] == "spec"
    assert metadata["canonical_document"] == "true"


# HTML-POC-UT-002
def test_parse_llm_managed_block_returns_none_without_marker() -> None:
    markdown = """<!--
foo: bar
-->

# title
"""

    assert markdown_loader.parse_llm_managed_block(markdown) is None


# HTML-POC-UT-003
def test_extract_headings_extracts_markdown_headings() -> None:
    headings = markdown_loader.extract_headings(VALID_MARKDOWN)

    assert headings == ["テスト仕様", "目的"]


# HTML-POC-UT-004
def test_extract_sec_ids_only_extracts_existing_sec_ids() -> None:
    assert markdown_loader.extract_sec_ids(VALID_MARKDOWN) == []
    assert markdown_loader.extract_sec_ids(VALID_MARKDOWN_WITH_SEC_ID) == ["sec_abc123"]


# HTML-POC-UT-007
def test_load_markdown_documents_reads_valid_documents(tmp_path: Path) -> None:
    source = tmp_path / "docs" / "ja-JP" / "仕様" / "00_共通"
    source.mkdir(parents=True)
    (source / "01_テスト仕様.md").write_text(VALID_MARKDOWN, encoding="utf-8")

    documents = markdown_loader.load_markdown_documents(tmp_path / "docs" / "ja-JP")

    assert len(documents) == 1
    assert documents[0].doc_id == "doc-test-001"
    assert documents[0].canonical_title == "テスト仕様"
    assert documents[0].sec_ids == []
