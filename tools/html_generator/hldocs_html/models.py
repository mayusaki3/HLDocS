"""HLDocS HTML generator data models.

役割:
    Markdown 正本文書と Presentation Model 文書の抽出済み情報を保持する。

注意点:
    - 本 module は値オブジェクトのみを定義する。
    - sec_id は本文に存在するものだけを保持し、推測生成しない。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MarkdownDocument:
    """Markdown 正本文書の抽出済み情報を保持する。

    役割:
        HTML Document Page と Manifest entry の生成元データとなる。

    注意点:
        sec_id は本文中に存在するものだけを保持し、推測生成しない。
    """

    source_path: Path
    relative_source_path: str
    doc_id: str
    lang: str
    canonical_title: str
    document_type: str
    canonical_document: str
    source_hash: str
    headings: list[str]
    sec_ids: list[str]
    body: str


@dataclass(frozen=True)
class PresentationDocument:
    """文書単位の表示構成モデルを保持する。

    役割:
        Markdown 正本を HTML 上でどのように扱うかを制御する。

    注意点:
        本情報は operational input であり、canonical specification ではない。
    """

    doc_id: str
    presentation_policy: str
    overview: str | None
    policy_reason: str | None
    source_path: str | None
