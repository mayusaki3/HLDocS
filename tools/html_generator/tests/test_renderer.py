"""Tests for renderer."""

from __future__ import annotations

from pathlib import Path

from hldocs_html.markdown_loader import load_markdown_documents
from hldocs_html.renderer import (
    markdown_source_link,
    render_document_map,
    render_navigation_items,
    safe_slug,
)

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


def _load_single_document(tmp_path: Path):
    input_root = tmp_path / "docs" / "ja-JP"
    source = input_root / "仕様" / "00_共通"
    source.mkdir(parents=True)
    (source / "01_テスト仕様.md").write_text(VALID_MARKDOWN, encoding="utf-8")
    return load_markdown_documents(input_root)[0]


# HTML-POC-UT-005
def test_safe_slug_removes_spaces() -> None:
    slug = safe_slug("HTML Site Manifest 規約")

    assert " " not in slug
    assert slug == "HTML_Site_Manifest_規約"


# HTML-POC-UT-RD-001
def test_markdown_source_link_points_to_canonical_markdown(tmp_path: Path) -> None:
    document = _load_single_document(tmp_path)

    assert (
        markdown_source_link(document)
        == "../markdown/viewer.html?src=../../仕様/00_共通/01_テスト仕様.md"
    )


# HTML-POC-UT-RD-002
def test_render_navigation_items_links_generated_pages() -> None:
    html = render_navigation_items(
        [
            {
                "title": "テストNavigation",
                "children": [
                    {"title": "テスト仕様", "doc_id": "doc-test-001"},
                    {"title": "未生成仕様", "doc_id": "doc-missing"},
                ],
            }
        ],
        {
            "doc-test-001": {
                "output_html_path": "reference/doc-test-001.html",
            }
        },
    )

    assert "テストNavigation" in html
    assert '<a href="reference/doc-test-001.html">テスト仕様</a>' in html
    assert "未生成仕様" in html


# HTML-POC-UT-RD-003
def test_render_document_map_shows_generated_and_not_generated_documents() -> None:
    html = render_document_map(
        [
            {
                "profile": ["reference"],
                "canonical_title": "Generated 仕様",
                "doc_id": "doc-generated",
                "source_markdown": "仕様/generated.md",
                "output_html_path": "reference/doc-generated.html",
                "presentation_policy": "full_render",
            }
        ],
        [
            {
                "canonical_title": "Not Generated 仕様",
                "doc_id": "doc-not-generated",
                "source_markdown": "仕様/not_generated.md",
                "presentation_policy": "not_generated",
            }
        ],
    )

    assert "<h2>" not in html
    assert "Generated 仕様" in html
    assert '<a href="reference/doc-generated.html">HTML</a>' in html
    assert "Not Generated 仕様" in html
    assert "<td>-</td>" in html
