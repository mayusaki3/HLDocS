"""Manifest utilities for HLDocS HTML generator.

役割:
    HTML Site Manifest 生成と generated artifact の簡易検査を担当する。

注意点:
    - Manifest 内部リンクは存在する page_id のみに正規化する。
    - 空白入り生成パスは GitHub Pages 配置時の事故を避けるため検出する。
"""

from __future__ import annotations

import json
from pathlib import Path

from .constants import SUPPORTED_PRESENTATION_POLICIES


def write_manifest(
    output_root: Path,
    profiles: list[str],
    pages: list[dict[str, object]],
    generated_at: str,
    not_generated_documents: list[dict[str, object]],
) -> None:
    """HTML Site Manifest を生成する。"""

    manifest_dir = output_root / "manifest"
    manifest_dir.mkdir(parents=True, exist_ok=True)

    page_ids = {str(page["page_id"]) for page in pages}

    for page in pages:
        page["link_targets"] = [
            target for target in page.get("link_targets", []) if target in page_ids
        ]

    manifest = {
        "generated_at": generated_at,
        "profile": profiles,
        "presentation_policy_enum": sorted(SUPPORTED_PRESENTATION_POLICIES),
        "pages": pages,
        "not_generated_documents": not_generated_documents,
    }

    (manifest_dir / "site-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def ensure_no_space_paths(output_root: Path) -> None:
    """生成物のパスに空白が含まれないことを検査する。"""

    bad_paths = [path for path in output_root.rglob("*") if " " in path.name]

    if bad_paths:
        joined = "\n".join(str(path) for path in bad_paths)
        raise RuntimeError(f"Generated paths contain spaces:\n{joined}")
