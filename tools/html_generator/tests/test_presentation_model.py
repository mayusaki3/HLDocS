"""Tests for presentation_model."""

from __future__ import annotations

import json
from pathlib import Path

from hldocs_html.presentation_model import (
    load_navigation_model,
    load_presentation_documents,
)


# HTML-POC-UT-PM-001
def test_load_presentation_documents_reads_document_policy(tmp_path: Path) -> None:
    input_root = tmp_path / "docs" / "ja-JP"
    documents_dir = input_root / "HTMLドキュメント" / "Presentation-Model" / "documents"
    documents_dir.mkdir(parents=True)
    (documents_dir / "doc-test-001.json").write_text(
        json.dumps(
            {
                "doc_id": "doc-test-001",
                "presentation_policy": "link_only",
                "overview": "概要",
                "policy_reason": "理由",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    documents, has_model = load_presentation_documents(input_root)

    assert has_model is True
    assert documents["doc-test-001"].presentation_policy == "link_only"
    assert documents["doc-test-001"].overview == "概要"
    assert documents["doc-test-001"].policy_reason == "理由"


# HTML-POC-UT-PM-002
def test_load_navigation_model_reads_site_navigation(tmp_path: Path) -> None:
    input_root = tmp_path / "docs" / "ja-JP"
    navigation_dir = input_root / "HTMLドキュメント" / "Presentation-Model" / "site"
    navigation_dir.mkdir(parents=True)
    (navigation_dir / "navigation.json").write_text(
        json.dumps(
            {
                "items": [
                    {
                        "title": "テストNavigation",
                        "children": [
                            {"title": "テスト仕様", "doc_id": "doc-test-001"},
                        ],
                    }
                ]
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    navigation_model = load_navigation_model(input_root)

    assert navigation_model is not None
    assert navigation_model["items"][0]["title"] == "テストNavigation"
