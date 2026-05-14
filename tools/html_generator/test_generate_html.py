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


# HTML-POC-UT-013
def test_markdown_source_link_opens_in_new_tab(tmp_path: Path) -> None:
    """Markdown 正本リンクが別タブ表示用属性を持つこと。"""

    input_root = tmp_path / "docs" / "ja-JP"
    source = input_root / "仕様" / "00_共通"
    source.mkdir(parents=True)
    (source / "01_テスト仕様.md").write_text(VALID_MARKDOWN, encoding="utf-8")

    output_root = input_root / "HTMLドキュメント"
    generate_html.generate(input_root, output_root, ["overview", "reference"])

    reference_files = list((output_root / "reference").glob("*.html"))
    assert reference_files

    reference_html = reference_files[0].read_text(encoding="utf-8")
    assert 'target="_blank"' in reference_html
    assert 'rel="noopener noreferrer"' in reference_html


# HTML-POC-UT-014
def test_presentation_policy_controls_rendering(tmp_path: Path) -> None:
    """Presentation Model の policy に従い HTML 生成内容が分岐すること。"""

    input_root = tmp_path / "docs" / "ja-JP"
    source = input_root / "仕様" / "00_共通"
    source.mkdir(parents=True)

    markdown_cases = {
        "doc-full": ("01_full.md", "Full Render 仕様", "FULL_RENDER_BODY"),
        "doc-overview": ("02_overview.md", "Overview Only 仕様", "OVERVIEW_ONLY_BODY"),
        "doc-link": ("03_link.md", "Link Only 仕様", "LINK_ONLY_BODY"),
        "doc-not-generated": ("04_not_generated.md", "Not Generated 仕様", "NOT_GENERATED_BODY"),
    }
    for doc_id, (filename, title, body_marker) in markdown_cases.items():
        (source / filename).write_text(
            f"""<!--
HLDocS:LLM-MANAGED
doc_id: {doc_id}
lang: ja-JP
canonical_title: {title}
document_type: spec
canonical_document: true
-->

# {title}

## 目的

{body_marker}
""",
            encoding="utf-8",
        )

    presentation_documents = input_root / "HTMLドキュメント" / "Presentation-Model" / "documents"
    presentation_documents.mkdir(parents=True)
    policies = {
        "doc-full": "full_render",
        "doc-overview": "overview_only",
        "doc-link": "link_only",
        "doc-not-generated": "not_generated",
    }
    for doc_id, policy in policies.items():
        (presentation_documents / f"{doc_id}.json").write_text(
            json.dumps(
                {
                    "doc_id": doc_id,
                    "presentation_policy": policy,
                    "overview": f"{policy} overview",
                    "policy_reason": f"{policy} reason",
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    output_root = input_root / "HTMLドキュメント"
    generate_html.generate(input_root, output_root, ["overview", "reference"])

    full_html = (output_root / "reference" / "doc-full.html").read_text(encoding="utf-8")
    overview_html = (output_root / "reference" / "doc-overview.html").read_text(encoding="utf-8")
    link_html = (output_root / "reference" / "doc-link.html").read_text(encoding="utf-8")
    index_html = (output_root / "index.html").read_text(encoding="utf-8")
    manifest = json.loads((output_root / "manifest" / "site-manifest.json").read_text(encoding="utf-8"))

    assert "FULL_RENDER_BODY" in full_html
    assert "OVERVIEW_ONLY_BODY" not in overview_html
    assert "本文は HTML 化せず、概要と見出しのみ表示します。" in overview_html
    assert "LINK_ONLY_BODY" not in link_html
    assert "本文は HTML 化せず、Markdown 正本リンクを参照します。" in link_html
    assert not (output_root / "reference" / "doc-not-generated.html").exists()
    assert "Not Generated 仕様" in index_html
    assert "not_generated reason" in index_html

    pages_by_doc_id = {page["doc_id"]: page for page in manifest["pages"] if page.get("doc_id")}
    assert pages_by_doc_id["doc-full"]["presentation_policy"] == "full_render"
    assert pages_by_doc_id["doc-overview"]["presentation_policy"] == "overview_only"
    assert pages_by_doc_id["doc-link"]["presentation_policy"] == "link_only"
    assert "doc-not-generated" not in pages_by_doc_id
    assert {
        item["doc_id"] for item in manifest["not_generated_documents"]
    } == {"doc-not-generated"}
