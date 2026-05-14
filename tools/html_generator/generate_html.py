#!/usr/bin/env python3
"""HLDocS HTML Generator PoC CLI entrypoint.

役割:
    既存の `python tools/html_generator/generate_html.py` 実行経路を維持しつつ、
    実処理を `hldocs_html` package へ委譲する。

注意点:
    - 本ファイルは互換入口であり、主要ロジックは hldocs_html 配下へ分割する。
    - 既存テスト互換のため、旧 public API 名を re-export する。

引数:
    --input:
        入力ルートディレクトリ。例: docs/ja-JP
    --output:
        HTML 出力先ディレクトリ。例: docs/ja-JP/HTMLドキュメント
    --profile:
        生成 profile のカンマ区切り。初期対応: overview,reference

戻り値:
    プロセス終了コード 0:
        生成成功。
    プロセス終了コード 1:
        入力不正または生成失敗。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from hldocs_html.constants import (
    DEFAULT_PROFILES,
    LEGACY_FALLBACK_POLICY,
    PRESENTATION_MODEL_DIR,
    PRESENTATION_MODEL_FALLBACK_POLICY,
    SUPPORTED_PRESENTATION_POLICIES,
    SUPPORTED_PROFILES,
)
from hldocs_html.generator import generate
from hldocs_html.manifest import ensure_no_space_paths, write_manifest
from hldocs_html.markdown_loader import (
    calculate_hash,
    extract_headings,
    extract_sec_ids,
    find_markdown_files,
    load_markdown_documents,
    parse_llm_managed_block,
)
from hldocs_html.models import MarkdownDocument, PresentationDocument
from hldocs_html.presentation_model import (
    load_navigation_model,
    load_presentation_documents,
    presentation_model_root,
    resolve_presentation_policy,
    validate_presentation_policy,
)
from hldocs_html.renderer import (
    build_reference_body,
    html_page,
    markdown_source_link,
    markdown_to_basic_html,
    reference_filename,
    render_document_map,
    render_navigation_items,
    safe_slug,
    write_index_page,
    write_overview_page,
    write_reference_pages,
)


def parse_args(argv: list[str]) -> argparse.Namespace:
    """CLI 引数を解析する。

    引数:
        argv: コマンドライン引数。

    戻り値:
        argparse.Namespace: 解析済み引数。
    """

    parser = argparse.ArgumentParser(description="Generate HLDocS HTML PoC output.")
    parser.add_argument("--input", required=True, help="Input docs root directory.")
    parser.add_argument("--output", required=True, help="Output HTML directory.")
    parser.add_argument(
        "--profile",
        default=",".join(DEFAULT_PROFILES),
        help="Comma-separated profiles. Supported: overview,reference.",
    )
    return parser.parse_args(argv)


def parse_profiles(raw_profiles: str) -> list[str]:
    """profile 指定を検証する。

    引数:
        raw_profiles: カンマ区切り profile 指定。

    戻り値:
        list[str]: profile 名一覧。

    例外:
        ValueError: 未対応 profile が指定された場合。
    """

    profiles = [item.strip() for item in raw_profiles.split(",") if item.strip()]

    if not profiles:
        profiles = DEFAULT_PROFILES.copy()

    unsupported = sorted(set(profiles) - SUPPORTED_PROFILES)

    if unsupported:
        raise ValueError(f"Unsupported profile(s): {', '.join(unsupported)}")

    return profiles


def main(argv: list[str]) -> int:
    """エントリーポイント。

    引数:
        argv: コマンドライン引数。

    戻り値:
        int: 終了コード。
    """

    try:
        args = parse_args(argv)
        profiles = parse_profiles(args.profile)
        generate(Path(args.input), Path(args.output), profiles)
        return 0
    except Exception as exc:  # noqa: BLE001 - CLI PoC のため例外内容を stderr へ集約する。
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


__all__ = [
    "DEFAULT_PROFILES",
    "LEGACY_FALLBACK_POLICY",
    "MarkdownDocument",
    "PRESENTATION_MODEL_DIR",
    "PRESENTATION_MODEL_FALLBACK_POLICY",
    "PresentationDocument",
    "SUPPORTED_PRESENTATION_POLICIES",
    "SUPPORTED_PROFILES",
    "build_reference_body",
    "calculate_hash",
    "ensure_no_space_paths",
    "extract_headings",
    "extract_sec_ids",
    "find_markdown_files",
    "generate",
    "html_page",
    "load_markdown_documents",
    "load_navigation_model",
    "load_presentation_documents",
    "main",
    "markdown_source_link",
    "markdown_to_basic_html",
    "parse_args",
    "parse_llm_managed_block",
    "parse_profiles",
    "presentation_model_root",
    "reference_filename",
    "render_document_map",
    "render_navigation_items",
    "resolve_presentation_policy",
    "safe_slug",
    "validate_presentation_policy",
    "write_index_page",
    "write_manifest",
    "write_overview_page",
    "write_reference_pages",
]


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
