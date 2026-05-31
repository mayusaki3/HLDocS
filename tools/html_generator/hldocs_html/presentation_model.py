"""Presentation Model utilities for HLDocS HTML generator.

役割:
    Presentation Model の読み込みと presentation_policy 解決を担当する。

注意点:
    - Presentation Model は operational input であり canonical ではない。
    - Presentation Model が未配置の場合は legacy fallback を使用する。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .constants import (
    LEGACY_FALLBACK_POLICY,
    PRESENTATION_MODEL_DIR,
    PRESENTATION_MODEL_FALLBACK_POLICY,
    SUPPORTED_PRESENTATION_POLICIES,
)
from .models import MarkdownDocument, PresentationDocument


def presentation_model_root(input_root: Path) -> Path:
    """表示構成モデルの配置ルートを返す。"""

    return input_root / "HTMLドキュメント" / PRESENTATION_MODEL_DIR


def validate_presentation_policy(policy: str) -> str:
    """presentation_policy を検証する。"""

    if policy not in SUPPORTED_PRESENTATION_POLICIES:
        supported = ", ".join(sorted(SUPPORTED_PRESENTATION_POLICIES))
        raise ValueError(
            f"Unsupported presentation_policy: {policy}. Supported: {supported}"
        )

    return policy


def load_presentation_documents(
    input_root: Path,
) -> tuple[dict[str, PresentationDocument], bool]:
    """文書単位の表示構成モデルを読み込む。"""

    root = presentation_model_root(input_root)

    if not root.exists():
        return {}, False

    documents_dir = root / "documents"

    if not documents_dir.exists():
        return {}, True

    presentation_documents: dict[str, PresentationDocument] = {}

    for path in sorted(documents_dir.glob("*.json")):
        raw: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))

        doc_id = str(raw.get("doc_id", "")).strip()

        if not doc_id:
            raise ValueError(f"Presentation Model document missing doc_id: {path}")

        policy = validate_presentation_policy(
            str(
                raw.get(
                    "presentation_policy",
                    PRESENTATION_MODEL_FALLBACK_POLICY,
                )
            )
        )

        presentation_documents[doc_id] = PresentationDocument(
            doc_id=doc_id,
            presentation_policy=policy,
            overview=raw.get("overview") if raw.get("overview") is not None else None,
            policy_reason=(
                raw.get("policy_reason")
                if raw.get("policy_reason") is not None
                else None
            ),
            source_path=path.relative_to(input_root).as_posix(),
        )

    return presentation_documents, True


def resolve_presentation_policy(
    document: MarkdownDocument,
    presentation_documents: dict[str, PresentationDocument],
    has_presentation_model: bool,
) -> str:
    """文書の presentation_policy を決定する。"""

    presentation_document = presentation_documents.get(document.doc_id)

    if presentation_document is not None:
        return presentation_document.presentation_policy

    if has_presentation_model:
        return PRESENTATION_MODEL_FALLBACK_POLICY

    return LEGACY_FALLBACK_POLICY


def load_navigation_model(input_root: Path) -> dict[str, Any] | None:
    """site/navigation.json を読み込む。"""

    path = presentation_model_root(input_root) / "site" / "navigation.json"

    if not path.exists():
        return None

    return json.loads(path.read_text(encoding="utf-8"))
