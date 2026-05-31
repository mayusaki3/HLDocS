"""Markdown viewer asset writer."""

from __future__ import annotations

from pathlib import Path

from .viewer_template import VIEWER_HTML


def markdown_viewer_link(markdown_source_path: str) -> str:
    """reference ページから Markdown viewer への相対リンクを生成する。"""

    return f"../markdown/viewer.html?src={markdown_source_path}"


def write_markdown_viewer_assets(output_root: Path) -> None:
    """Markdown viewer assets を生成する。"""

    viewer_dir = output_root / "markdown"
    viewer_dir.mkdir(parents=True, exist_ok=True)

    package_dir = Path(__file__).parent

    (viewer_dir / "viewer.html").write_text(VIEWER_HTML, encoding="utf-8")
    (viewer_dir / "viewer.css").write_text(
        (package_dir / "viewer.css").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    viewer_js = package_dir / "viewer.js"

    if viewer_js.exists():
        (viewer_dir / "viewer.js").write_text(
            viewer_js.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
