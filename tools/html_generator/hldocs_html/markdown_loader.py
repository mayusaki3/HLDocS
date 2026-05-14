"""Markdown loading utilities for HLDocS HTML generator.

役割:
    Markdown 正本文書の探索、metadata 抽出、Document model 化を担当する。

注意点:
    - Markdown 正本を canonical として扱う。
    - sec_id は本文に存在するものだけを抽出し、推測生成しない。
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from .models import MarkdownDocument


def calculate_hash(text: str) -> str:
    """文字列の SHA-256 hash を返す。"""

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def find_markdown_files(input_root: Path) -> list[Path]:
    """入力ルート配下の Markdown ファイルを列挙する。"""

    excluded_parts = {"HTMLドキュメント", ".git"}
    files: list[Path] = []

    for path in sorted(input_root.rglob("*.md")):
        if any(part in excluded_parts for part in path.parts):
            continue
        files.append(path)

    return files


def parse_llm_managed_block(text: str) -> dict[str, str] | None:
    """LLM-MANAGED ブロックを抽出する。"""

    match = re.match(r"\s*<!--\s*(.*?)\s*-->\s*", text, flags=re.DOTALL)
    if not match:
        return None

    block = match.group(1)
    if "HLDocS:LLM-MANAGED" not in block:
        return None

    metadata: dict[str, str] = {}

    for line in block.splitlines():
        stripped = line.strip()

        if not stripped or stripped == "HLDocS:LLM-MANAGED":
            continue

        if ":" not in stripped:
            continue

        key, value = stripped.split(":", 1)
        metadata[key.strip()] = value.strip()

    return metadata


def extract_headings(text: str) -> list[str]:
    """Markdown 見出しを抽出する。"""

    headings: list[str] = []

    for line in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match:
            headings.append(match.group(2))

    return headings


def extract_sec_ids(text: str) -> list[str]:
    """本文に存在する sec_id を抽出する。"""

    return sorted(set(re.findall(r"\bsec_(?!id\b)[A-Za-z0-9][A-Za-z0-9_-]*\b", text)))


def load_markdown_documents(input_root: Path) -> list[MarkdownDocument]:
    """Markdown 正本文書を読み込み、metadata を抽出する。"""

    documents: list[MarkdownDocument] = []

    for path in find_markdown_files(input_root):
        text = path.read_text(encoding="utf-8")
        metadata = parse_llm_managed_block(text)

        if metadata is None:
            continue

        required_keys = [
            "doc_id",
            "lang",
            "canonical_title",
            "document_type",
            "canonical_document",
        ]

        if any(key not in metadata for key in required_keys):
            continue

        relative_source = path.relative_to(input_root).as_posix()

        documents.append(
            MarkdownDocument(
                source_path=path,
                relative_source_path=relative_source,
                doc_id=metadata["doc_id"],
                lang=metadata["lang"],
                canonical_title=metadata["canonical_title"],
                document_type=metadata["document_type"],
                canonical_document=metadata["canonical_document"],
                source_hash=calculate_hash(text),
                headings=extract_headings(text),
                sec_ids=extract_sec_ids(text),
                body=text,
            )
        )

    return documents
