"""
HLDocS Markdown Viewer Template

Responsibilities:
- lightweight markdown browsing
- render/source layout
- TOC layout
- Mermaid bootstrap

Non-responsibilities:
- graph runtime
- projection runtime
- distributed synchronization
- operational orchestration
"""

from pathlib import Path


TEMPLATE_DIR = Path(__file__).parent / "templates"


def load_viewer_template() -> str:
    """
    Load standalone viewer HTML template.

    Returns:
        HTML template text.
    """

    template_path = TEMPLATE_DIR / "viewer.html"

    return template_path.read_text(encoding="utf-8")
