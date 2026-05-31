"""Markdown viewer package.

役割:
    Markdown viewer の template / style / script / asset 書き出しを提供する。
"""

from .assets import markdown_viewer_link, write_markdown_viewer_assets

__all__ = ["markdown_viewer_link", "write_markdown_viewer_assets"]
