"""
HLDocS HTML Generator PoC tests.

役割:
    tools/html_generator/generate_html.py の PoC 動作を検証する。

注意点:
    - 本テストは PoC 用の最小テストである。
    - 生成 HTML の見た目ではなく、HLDocS の仕様上重要な制約を検証する。
    - sec_id は推測生成せず、本文に存在するものだけを抽出する。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_html  # noqa: E402


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
    """LLM-MANAGED ブロックから必須 metadata を抽出できること。"""

    metadata = generate_html.parse_llm_managed_block(VALID_MARKDOWN)

    assert metadata is not None
    assert metadata["doc_id"] == "doc-test-001"
    assert metadata["lang"] == "ja-JP"
    assert metadata["canonical_title"] == "テスト仕様"
    assert metadata["document_type"] == "spec"
    assert metadata["canonical_document"] == "true"


# HTML-POC-UT-002
def test_parse_llm_managed_block_returns_none_without_marker() -> None:
    """HLDocS marker がない HTML comment は metadata として扱わないこと。"""

    markdown = """<!--
foo: bar
-->

# title
"""

    assert generate_html.parse_llm_managed_block(markdown) is None


# HTML-POC-UT-003
def test_extract_headings_extracts_markdown_headings() -> None:
    """Markdown 見出しを抽出できること。"""

    headings = generate_html.extract_headings(VALID_MARKDOWN)

    assert headings == ["テスト仕様", "目的"]


# HTML-POC-UT-004
def test_extract_sec_ids_only_extracts_existing_sec_ids() -> None:
    """本文に存在する sec_id のみ抽出し、存在しない sec_id を推測しないこと。"""

    assert generate_html.extract_sec_ids(VALID_MARKDOWN) == []
    assert generate_html.extract_sec_ids(VALID_MARKDOWN_WITH_SEC_ID) == ["sec_abc123"]


# HTML-POC-UT-005
def test_safe_slug_removes_spaces() -> None:
    """HTML ファイル名用 slug が空白を含まないこと。"""

    slug = generate_html.safe_slug("HTML Site Manifest 規約")

    assert " " not in slug
    assert slug == "HTML_Site_Manifest_規約"


# HTML-POC-UT-006
def test_parse_profiles_rejects_unsupported_profile() -> None:
    """未対応 profile を拒否すること。"""

    with pytest.raises(ValueError):
        generate_html.parse_profiles("overview,test-report")


# HTML-POC-UT-007
def test_load_markdown_documents_reads_valid_documents(tmp_path: Path) -> None:
    """Markdown 正本文書を読み込み、必要 metadata を抽出できること。"""

    source = tmp_path / "docs" / "ja-JP" / "仕様" / "00_共通"
    source.mkdir(parents=True)
    (source / "01_テスト仕様.md").write_text(VALID_MARKDOWN, encoding="utf-8")

    documents = generate_html.load_markdown_documents(tmp_path / "docs" / "ja-JP")

    assert len(documents) == 1
    assert documents[0].doc_id == "doc-test-001"
    assert documents[0].canonical_title == "テスト仕様"
    assert documents[0].sec_ids == []


# HTML-POC-UT-008
def test_generate_outputs_index_overview_reference_and_manifest(tmp_path: Path) -> None:
    """overview/reference/manifest/index が生成されること。"""

    input_root = tmp_path / "docs" / "ja-JP"
    source = input_root / "仕様" / "00_共通"
    source.mkdir(parents=True)
    (source / "01_テスト仕様.md").write_text(VALID_MARKDOWN, encoding="utf-8")

    output_root = input_root / "HTMLドキュメント"

    generate_html.generate(input_root, output_root, ["overview", "reference"])

    assert (output_root / "index.html").exists()
    assert (output_root / "overview" / "index.html").exists()
    assert list((output_root / "reference").glob("*.html"))
    assert (output_root / "manifest" / "site-manifest.json").exists()


# HTML-POC-UT-009
def test_manifest_contains_required_page_fields(tmp_path: Path) -> None:
    """Manifest page entry が必須項目を持つこと。"""

    input_root = tmp_path / "docs" / "ja-JP"
    source = input_root / "仕様" / "00_共通"
    source.mkdir(parents=True)
    (source / "01_テスト仕様.md").write_text(VALID_MARKDOWN, encoding="utf-8")

    output_root = input_root / "HTMLドキュメント"
    generate_html.generate(input_root, output_root, ["overview", "reference"])

    manifest = json.loads((output_root / "manifest" / "site-manifest.json").read_text(encoding="utf-8"))
    assert manifest["profile"] == ["overview", "reference"]
    assert manifest["pages"]

    required_keys = {
        "page_id",
        "profile",
        "source_markdown",
        "canonical_title",
        "doc_id",
        "sec_id",
        "output_html_path",
        "source_hash",
        "stale",
        "link_targets",
    }
    for page in manifest["pages"]:
        assert required_keys.issubset(page.keys())


# HTML-POC-UT-010
def test_generated_paths_do_not_contain_spaces(tmp_path: Path) -> None:
    """HTML generated artifact に空白入りファイル名が生成されないこと。"""

    input_root = tmp_path / "docs" / "ja-JP"
    source = input_root / "仕様" / "00_共通"
    source.mkdir(parents=True)
    (source / "01_テスト仕様.md").write_text(VALID_MARKDOWN, encoding="utf-8")

    output_root = input_root / "HTMLドキュメント"
    generate_html.generate(input_root, output_root, ["overview", "reference"])

    assert [path for path in output_root.rglob("*") if " " in path.name] == []


# HTML-POC-UT-011
def test_not_generated_is_displayed_in_index(tmp_path: Path) -> None:
    """PoC-1 対象外 profile が not generated として表示されること。"""

    input_root = tmp_path / "docs" / "ja-JP"
    source = input_root / "仕様" / "00_共通"
    source.mkdir(parents=True)
    (source / "01_テスト仕様.md").write_text(VALID_MARKDOWN, encoding="utf-8")

    output_root = input_root / "HTMLドキュメント"
    generate_html.generate(input_root, output_root, ["overview", "reference"])

    index_html = (output_root / "index.html").read_text(encoding="utf-8")
    assert "Not generated" in index_html
    assert "traceability" in index_html
    assert "test-report" in index_html


# HTML-POC-UT-012
def test_manifest_link_targets_only_reference_existing_pages(tmp_path: Path) -> None:
    """Manifest の link_targets が存在する page_id のみを参照すること。"""

    input_root = tmp_path / "docs" / "ja-JP"
    source = input_root / "仕様" / "00_共通"
    source.mkdir(parents=True)
    (source / "01_テスト仕様.md").write_text(VALID_MARKDOWN, encoding="utf-8")

    output_root = input_root / "HTMLドキュメント"
    generate_html.generate(input_root, output_root, ["overview", "reference"])

    manifest = json.loads((output_root / "manifest" / "site-manifest.json").read_text(encoding="utf-8"))
    page_ids = {page["page_id"] for page in manifest["pages"]}
    for page in manifest["pages"]:
        assert set(page["link_targets"]).issubset(page_ids)
