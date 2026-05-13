#!/usr/bin/env python3
"""
HLDocS HTML Generator PoC.

役割:
    HLDocS の Markdown 正本文書群から、最小限の HTML ドキュメント、
    overview、index、HTML Site Manifest を生成する。

注意点:
    - 本スクリプトは PoC 用の最小実装である。
    - Markdown 正本を canonical とし、HTML は read-only Operational Representation として生成する。
    - sec_id は Markdown 本文に存在する場合のみ抽出し、存在しない sec_id を推測生成しない。
    - Manifest に存在しないページへの HTML 内部リンクを生成しない。

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
import datetime as _datetime
import hashlib
import html
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SUPPORTED_PROFILES = {"overview", "reference"}
DEFAULT_PROFILES = ["overview", "reference"]


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


def calculate_hash(text: str) -> str:
    """文字列の SHA-256 hash を返す。

    引数:
        text: 対象文字列。

    戻り値:
        str: SHA-256 hex digest。
    """

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def find_markdown_files(input_root: Path) -> list[Path]:
    """入力ルート配下の Markdown ファイルを列挙する。

    引数:
        input_root: 入力ルートディレクトリ。

    戻り値:
        list[Path]: Markdown ファイル一覧。
    """

    excluded_parts = {"HTMLドキュメント", ".git"}
    files: list[Path] = []
    for path in sorted(input_root.rglob("*.md")):
        if any(part in excluded_parts for part in path.parts):
            continue
        files.append(path)
    return files


def parse_llm_managed_block(text: str) -> dict[str, str] | None:
    """LLM-MANAGED ブロックを抽出する。

    引数:
        text: Markdown 本文。

    戻り値:
        dict[str, str] | None: 抽出できた metadata。存在しない場合 None。
    """

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
    """Markdown 見出しを抽出する。

    引数:
        text: Markdown 本文。

    戻り値:
        list[str]: 見出し文字列一覧。
    """

    headings: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match:
            headings.append(match.group(2))
    return headings


def extract_sec_ids(text: str) -> list[str]:
    """本文に存在する sec_id を抽出する。

    引数:
        text: Markdown 本文。

    戻り値:
        list[str]: 本文に存在する sec_id 一覧。
    """

    return sorted(set(re.findall(r"\bsec_[A-Za-z0-9_-]+\b", text)))


def load_markdown_documents(input_root: Path) -> list[MarkdownDocument]:
    """Markdown 正本文書を読み込み、metadata を抽出する。

    引数:
        input_root: 入力ルートディレクトリ。

    戻り値:
        list[MarkdownDocument]: 抽出済み文書一覧。
    """

    documents: list[MarkdownDocument] = []
    for path in find_markdown_files(input_root):
        text = path.read_text(encoding="utf-8")
        metadata = parse_llm_managed_block(text)
        if metadata is None:
            continue

        required_keys = ["doc_id", "lang", "canonical_title", "document_type", "canonical_document"]
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


def safe_slug(value: str) -> str:
    """HTML ファイル名に使う安全な slug を生成する。

    引数:
        value: 元文字列。

    戻り値:
        str: 空白を含まない slug。
    """

    normalized = re.sub(r"\s+", "_", value.strip())
    normalized = re.sub(r"[^0-9A-Za-z_\-\u3040-\u30ff\u3400-\u9fff]+", "_", normalized)
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized or "document"


def reference_filename(document: MarkdownDocument) -> str:
    """Document Page のファイル名を生成する。

    引数:
        document: 対象 Markdown 文書。

    戻り値:
        str: HTML ファイル名。
    """

    return f"{safe_slug(document.doc_id)}.html"


def markdown_to_basic_html(markdown_text: str) -> str:
    """Markdown を最小 HTML へ変換する。

    引数:
        markdown_text: Markdown 本文。

    戻り値:
        str: 最小変換 HTML。

    注意点:
        PoC 用の簡易変換であり、完全な Markdown 変換器ではない。
    """

    lines: list[str] = []
    in_code_block = False
    code_buffer: list[str] = []

    for raw_line in markdown_text.splitlines():
        line = raw_line.rstrip("\n")
        if line.startswith("```"):
            if in_code_block:
                lines.append("<pre><code>" + html.escape("\n".join(code_buffer)) + "</code></pre>")
                code_buffer = []
                in_code_block = False
            else:
                in_code_block = True
            continue

        if in_code_block:
            code_buffer.append(line)
            continue

        heading = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if heading:
            level = len(heading.group(1))
            title = html.escape(heading.group(2))
            lines.append(f"<h{level}>{title}</h{level}>")
        elif not line.strip():
            lines.append("")
        elif line.startswith("- "):
            lines.append(f"<p>• {html.escape(line[2:])}</p>")
        else:
            lines.append(f"<p>{html.escape(line)}</p>")

    if in_code_block:
        lines.append("<pre><code>" + html.escape("\n".join(code_buffer)) + "</code></pre>")

    return "\n".join(lines)


def html_page(title: str, body_html: str) -> str:
    """HTML ページ全体を生成する。

    引数:
        title: HTML title。
        body_html: body 内 HTML。

    戻り値:
        str: 完整 HTML。
    """

    escaped_title = html.escape(title)
    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escaped_title}</title>
  <style>
    body {{ font-family: sans-serif; line-height: 1.7; margin: 2rem; max-width: 1080px; }}
    header, nav, main, footer {{ margin-bottom: 1.5rem; }}
    code, pre {{ background: #f5f5f5; }}
    pre {{ padding: 1rem; overflow-x: auto; }}
    .meta {{ border: 1px solid #ddd; padding: 1rem; background: #fafafa; }}
    .warning {{ border: 1px solid #d99; padding: 1rem; background: #fff7f7; }}
    a {{ text-decoration: none; }}
  </style>
</head>
<body>
{body_html}
</body>
</html>
"""


def write_reference_pages(output_root: Path, input_root: Path, documents: list[MarkdownDocument]) -> list[dict[str, object]]:
    """reference HTML と Manifest page entries を生成する。

    引数:
        output_root: 出力ルート。
        input_root: 入力ルート。
        documents: Markdown 文書一覧。

    戻り値:
        list[dict[str, object]]: Manifest page entries。
    """

    reference_dir = output_root / "reference"
    reference_dir.mkdir(parents=True, exist_ok=True)

    pages: list[dict[str, object]] = []
    for document in documents:
        output_name = reference_filename(document)
        output_path = reference_dir / output_name
        source_link = Path("../..") / document.relative_source_path
        heading_items = "".join(f"<li>{html.escape(item)}</li>" for item in document.headings)
        body_html = f"""
<header>
  <h1>{html.escape(document.canonical_title)}</h1>
  <p><a href="../index.html">HTMLドキュメント index</a></p>
</header>
<main>
  <section class="meta">
    <p><strong>doc_id:</strong> {html.escape(document.doc_id)}</p>
    <p><strong>document_type:</strong> {html.escape(document.document_type)}</p>
    <p><strong>canonical_document:</strong> {html.escape(document.canonical_document)}</p>
    <p><strong>Markdown正本:</strong> <a href="{html.escape(source_link.as_posix())}">{html.escape(document.canonical_title)}</a></p>
  </section>
  <section>
    <h2>見出し一覧</h2>
    <ul>{heading_items}</ul>
  </section>
  <section>
    <h2>本文</h2>
    {markdown_to_basic_html(document.body)}
  </section>
</main>
"""
        output_path.write_text(html_page(document.canonical_title, body_html), encoding="utf-8")
        pages.append(
            {
                "page_id": f"reference:{document.doc_id}",
                "profile": ["reference"],
                "source_markdown": document.relative_source_path,
                "canonical_title": document.canonical_title,
                "doc_id": document.doc_id,
                "sec_id": document.sec_ids,
                "output_html_path": output_path.relative_to(output_root).as_posix(),
                "source_hash": document.source_hash,
                "stale": False,
                "link_targets": [],
            }
        )
    return pages


def write_overview_page(output_root: Path, documents: list[MarkdownDocument]) -> dict[str, object]:
    """overview HTML と Manifest page entry を生成する。

    引数:
        output_root: 出力ルート。
        documents: Markdown 文書一覧。

    戻り値:
        dict[str, object]: Manifest page entry。
    """

    overview_dir = output_root / "overview"
    overview_dir.mkdir(parents=True, exist_ok=True)
    output_path = overview_dir / "index.html"

    by_type: dict[str, int] = {}
    for document in documents:
        by_type[document.document_type] = by_type.get(document.document_type, 0) + 1

    type_items = "".join(f"<li>{html.escape(key)}: {value}</li>" for key, value in sorted(by_type.items()))
    body_html = f"""
<header>
  <h1>HLDocS HTML Overview</h1>
  <p><a href="../index.html">HTMLドキュメント index</a></p>
</header>
<main>
  <section>
    <h2>目的</h2>
    <p>HLDocS Markdown 正本から生成された overview HTML です。</p>
  </section>
  <section>
    <h2>生成範囲</h2>
    <ul>
      <li>overview: generated</li>
      <li>reference: generated</li>
      <li>traceability: not generated</li>
      <li>test-report: not generated</li>
    </ul>
  </section>
  <section>
    <h2>document_type 集計</h2>
    <ul>{type_items}</ul>
  </section>
  <section class="warning">
    <h2>注意</h2>
    <p>HTML は read-only Operational Representation であり、Markdown 正本ではありません。</p>
  </section>
</main>
"""
    output_path.write_text(html_page("HLDocS HTML Overview", body_html), encoding="utf-8")
    return {
        "page_id": "overview:index",
        "profile": ["overview"],
        "source_markdown": None,
        "canonical_title": "HLDocS HTML Overview",
        "doc_id": None,
        "sec_id": [],
        "output_html_path": output_path.relative_to(output_root).as_posix(),
        "source_hash": None,
        "stale": False,
        "link_targets": [],
    }


def write_index_page(output_root: Path, pages: list[dict[str, object]], generated_at: str) -> None:
    """HTML ドキュメント入口 index.html を生成する。

    引数:
        output_root: 出力ルート。
        pages: Manifest page entries。
        generated_at: 生成日時。
    """

    reference_items: list[str] = []
    for page in pages:
        if "reference" not in page.get("profile", []):
            continue
        title = str(page["canonical_title"])
        path = str(page["output_html_path"])
        reference_items.append(f"<li><a href=\"{html.escape(path)}\">{html.escape(title)}</a></li>")

    body_html = f"""
<header>
  <h1>HLDocS HTMLドキュメント</h1>
</header>
<main>
  <section class="meta">
    <p><strong>generated_at:</strong> {html.escape(generated_at)}</p>
    <p><strong>profile:</strong> overview, reference</p>
  </section>
  <section>
    <h2>Overview</h2>
    <p><a href="overview/index.html">HLDocS HTML Overview</a></p>
  </section>
  <section>
    <h2>Reference</h2>
    <ul>{''.join(reference_items)}</ul>
  </section>
  <section>
    <h2>Not generated</h2>
    <ul>
      <li>traceability</li>
      <li>test-report</li>
    </ul>
  </section>
</main>
"""
    (output_root / "index.html").write_text(html_page("HLDocS HTMLドキュメント", body_html), encoding="utf-8")


def write_manifest(output_root: Path, profiles: list[str], pages: list[dict[str, object]], generated_at: str) -> None:
    """HTML Site Manifest を生成する。

    引数:
        output_root: 出力ルート。
        profiles: 生成 profile。
        pages: Manifest page entries。
        generated_at: 生成日時。
    """

    manifest_dir = output_root / "manifest"
    manifest_dir.mkdir(parents=True, exist_ok=True)

    page_ids = {str(page["page_id"]) for page in pages}
    for page in pages:
        page["link_targets"] = [target for target in page.get("link_targets", []) if target in page_ids]

    manifest = {
        "generated_at": generated_at,
        "profile": profiles,
        "pages": pages,
    }
    (manifest_dir / "site-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def ensure_no_space_paths(output_root: Path) -> None:
    """生成物のパスに空白が含まれないことを検査する。

    引数:
        output_root: 出力ルート。

    例外:
        RuntimeError: 空白入りパスを検出した場合。
    """

    bad_paths = [path for path in output_root.rglob("*") if " " in path.name]
    if bad_paths:
        joined = "\n".join(str(path) for path in bad_paths)
        raise RuntimeError(f"Generated paths contain spaces:\n{joined}")


def generate(input_root: Path, output_root: Path, profiles: list[str]) -> None:
    """HTML PoC 生成を実行する。

    引数:
        input_root: 入力ルート。
        output_root: 出力ルート。
        profiles: 生成 profile。
    """

    if not input_root.exists() or not input_root.is_dir():
        raise ValueError(f"Input directory does not exist: {input_root}")

    output_root.mkdir(parents=True, exist_ok=True)
    documents = load_markdown_documents(input_root)
    generated_at = _datetime.datetime.now(_datetime.UTC).isoformat()

    pages: list[dict[str, object]] = []
    if "reference" in profiles:
        pages.extend(write_reference_pages(output_root, input_root, documents))
    if "overview" in profiles:
        pages.append(write_overview_page(output_root, documents))

    write_index_page(output_root, pages, generated_at)
    write_manifest(output_root, profiles, pages, generated_at)
    ensure_no_space_paths(output_root)


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


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
