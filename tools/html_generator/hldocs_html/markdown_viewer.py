"""Compatibility wrapper for Markdown viewer asset generation.

役割:
    既存 import 経路 `hldocs_html.markdown_viewer` を維持しつつ、
    実装を `hldocs_html.markdown_viewer` package へ委譲する。

注意点:
    - 新規実装は `hldocs_html/markdown_viewer/` 配下に追加する。
    - 本ファイルには viewer template / CSS / JS を直接保持しない。
"""

from __future__ import annotations

from .markdown_viewer import markdown_viewer_link, write_markdown_viewer_assets

__all__ = ["markdown_viewer_link", "write_markdown_viewer_assets"]
