"""HLDocS HTML generator orchestration.

役割:
    Markdown loader / Presentation Model / renderer / manifest を統合し、
    HTML generated artifact 一式を生成する。

注意点:
    - Markdown 正本を canonical として扱う。
    - HTML は read-only Operational Representation として扱う。
"""

from __future__ import annotations

import datetime as _datetime
from pathlib import Path

from .manifest import ensure_no_space_paths, write_manifest
from .markdown_loader import load_markdown_documents
from .presentation_model import (
    load_navigation_model,
    load_presentation_documents,
)
from .renderer import (
    write_index_page,
    write_overview_page,
    write_reference_pages,
)


def generate(input_root: Path, output_root: Path, profiles: list[str]) -> None:
    """HTML PoC 生成を実行する。"""

    if not input_root.exists() or not input_root.is_dir():
        raise ValueError(f"Input directory does not exist: {input_root}")

    output_root.mkdir(parents=True, exist_ok=True)

    documents = load_markdown_documents(input_root)
    presentation_documents, has_presentation_model = load_presentation_documents(
        input_root
    )
    navigation_model = load_navigation_model(input_root)

    generated_at = _datetime.datetime.now(_datetime.UTC).isoformat()

    pages: list[dict[str, object]] = []
    not_generated_documents: list[dict[str, object]] = []

    if "reference" in profiles:
        reference_pages, not_generated_documents = write_reference_pages(
            output_root,
            documents,
            presentation_documents,
            has_presentation_model,
        )
        pages.extend(reference_pages)

    if "overview" in profiles:
        pages.append(write_overview_page(output_root, documents))

    write_index_page(
        output_root,
        pages,
        generated_at,
        not_generated_documents,
        navigation_model,
    )

    write_manifest(
        output_root,
        profiles,
        pages,
        generated_at,
        not_generated_documents,
    )

    ensure_no_space_paths(output_root)
