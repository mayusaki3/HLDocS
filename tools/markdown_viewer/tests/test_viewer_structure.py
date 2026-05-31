"""
Tests for markdown_viewer architectural boundaries.

These tests intentionally validate that markdown_viewer
remains a lightweight Browse layer.
"""

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


FORBIDDEN_KEYWORDS = [
    "RuntimeManager",
    "ProjectionEngine",
    "CapabilityRegistry",
    "RendererPipeline",
    "DistributedState",
    "SynchronizationContext",
    "GraphRuntime",
]


TARGET_FILES = [
    ROOT_DIR / "viewer.js",
    ROOT_DIR / "viewer_template.py",
]


def test_viewer_does_not_contain_runtime_abstractions():
    """
    Ensure markdown_viewer does not evolve into runtime platform.
    """

    for target_file in TARGET_FILES:
        content = target_file.read_text(encoding="utf-8")

        for keyword in FORBIDDEN_KEYWORDS:
            assert keyword not in content
