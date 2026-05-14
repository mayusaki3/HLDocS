"""HTML rendering utilities for HLDocS HTML generator.

役割:
    Markdown 正本と Presentation Model から HTML generated artifact を生成する。

注意点:
    - Markdown 正本を置換しない。
    - HTML は read-only Operational Representation として扱う。
    - Markdown 変換は PoC 用の最小変換であり、完全な Markdown viewer ではない。
"""

from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Any

from .markdown_viewer import markdown_viewer_link
from .models import MarkdownDocument, PresentationDocument
from .presentation_model import resolve_presentation_policy


def safe_slug(value: str) -> str:
    """HTML ファイル名に使う安全な slug を生成する。"""

    normalized = re.sub(r"\s+", "_", value.strip())
    normalized = re.sub(r"[^0-9A-Za-z_\-\u3040-\u30ff\u3400-\u9fff]+", "_", normalized)
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized or "document"


def reference_filename(document: MarkdownDocument) -> str:
    """Document Page のファイル名を生成する。"""

    return f"{safe_slug(document.doc_id)}.html"


def markdown_to_basic_html(markdown_text: str) -> str:
    """Markdown を最小 HTML へ変換する。"""

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
    """HTML ページ全体を生成する。"""

    escaped_title = html.escape(title)
    return f"""<!doctype html>
<html lang=\"ja\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{escaped_title}</title>
  <style>
    body {{ font-family: sans-serif; line-height: 1.7; margin: 2rem; max-width: 1080px; }}
    header, nav, main, footer {{ margin-bottom: 1.5rem; }}
    code, pre {{ background: #f5f5f5; }}
    pre {{ padding: 1rem; overflow-x: auto; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ddd; padding: 0.5rem; text-align: left; vertical-align: top; }}
    th {{ background: #f5f5f5; }}
    .meta {{ border: 1px solid #ddd; padding: 1rem; background: #fafafa; }}
    .warning {{ border: 1px solid #d99; padding: 1rem; background: #fff7f7; }}
    .card {{ border: 1px solid #ddd; padding: 1rem; margin: 1rem 0; }}
    a {{ text-decoration: none; }}
  </style>
</head>
<body>
{body_html}
</body>
</html>
"""


def markdown_source_link(document: MarkdownDocument) -> str:
    """reference ページから Markdown 正本 viewer への相対リンクを生成する。"""

    markdown_path = (Path("../..") / document.relative_source_path).as_posix()
    return markdown_viewer_link(markdown_path)


def build_reference_body(
    document: MarkdownDocument,
    presentation_document: PresentationDocument | None,
    policy: str,
) -> str:
    """presentation_policy に従い reference ページ本文を生成する。"""

    source_link = markdown_source_link(document)
    heading_items = "".join(f"<li>{html.escape(item)}</li>" for item in document.headings)
    overview = presentation_document.overview if presentation_document and presentation_document.overview else None
    reason = presentation_document.policy_reason if presentation_document and presentation_document.policy_reason else None

    common_html = f"""
<header>
  <h1>{html.escape(document.canonical_title)}</h1>
  <p><a href=\"../index.html\">HTMLドキュメント index</a></p>
</header>
<main>
  <section class=\"meta\">
    <p><strong>doc_id:</strong> {html.escape(document.doc_id)}</p>
    <p><strong>document_type:</strong> {html.escape(document.document_type)}</p>
    <p><strong>canonical_document:</strong> {html.escape(document.canonical_document)}</p>
    <p><strong>presentation_policy:</strong> {html.escape(policy)}</p>
    <p><strong>Markdown正本:</strong> <a href=\"{html.escape(source_link)}\" target=\"_blank\" rel=\"noopener noreferrer\">{html.escape(document.canonical_title)}</a></p>
  </section>
"""

    if overview:
        common_html += f"""
  <section>
    <h2>概要</h2>
    <p>{html.escape(overview)}</p>
  </section>
"""

    if reason:
        common_html += f"""
  <section>
    <h2>HTML表示方針の理由</h2>
    <p>{html.escape(reason)}</p>
  </section>
"""

    if policy == "link_only":
        return common_html + """
  <section>
    <h2>本文</h2>
    <p>本文は HTML 化せず、Markdown 正本リンクを参照します。</p>
  </section>
</main>
"""

    if policy == "overview_only":
        return common_html + f"""
  <section>
    <h2>見出し一覧</h2>
    <ul>{heading_items}</ul>
  </section>
  <section>
    <h2>本文</h2>
    <p>本文は HTML 化せず、概要と見出しのみ表示します。</p>
  </section>
</main>
"""

    return common_html + f"""
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


def write_reference_pages(
    output_root: Path,
    documents: list[MarkdownDocument],
    presentation_documents: dict[str, PresentationDocument],
    has_presentation_model: bool,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """reference HTML と Manifest page entries を生成する。"""

    reference_dir = output_root / "reference"
    reference_dir.mkdir(parents=True, exist_ok=True)

    pages: list[dict[str, object]] = []
    not_generated: list[dict[str, object]] = []

    for document in documents:
        policy = resolve_presentation_policy(
            document,
            presentation_documents,
            has_presentation_model,
        )
        presentation_document = presentation_documents.get(document.doc_id)

        if policy == "not_generated":
            not_generated.append(
                {
                    "doc_id": document.doc_id,
                    "canonical_title": document.canonical_title,
                    "source_markdown": document.relative_source_path,
                    "presentation_policy": policy,
                    "reason": presentation_document.policy_reason if presentation_document else None,
                }
            )
            continue

        output_name = reference_filename(document)
        output_path = reference_dir / output_name
        body_html = build_reference_body(document, presentation_document, policy)
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
                "presentation_policy": policy,
                "presentation_model": presentation_document.source_path if presentation_document else None,
            }
        )

    return pages, not_generated


def write_overview_page(
    output_root: Path,
    documents: list[MarkdownDocument],
) -> dict[str, object]:
    """overview HTML と Manifest page entry を生成する。"""

    overview_dir = output_root / "overview"
    overview_dir.mkdir(parents=True, exist_ok=True)
    output_path = overview_dir / "index.html"

    by_type: dict[str, int] = {}

    for document in documents:
        by_type[document.document_type] = by_type.get(document.document_type, 0) + 1

    type_items = "".join(
        f"<li>{html.escape(key)}: {value}</li>" for key, value in sorted(by_type.items())
    )

    body_html = f"""
<header>
  <h1>HLDocS HTML Overview</h1>
  <p><a href=\"../index.html\">HTMLドキュメント index</a></p>
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
  <section class=\"warning\">
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
        "presentation_policy": "generated",
        "presentation_model": None,
    }


def render_navigation_items(
    items: list[dict[str, Any]],
    pages_by_doc_id: dict[str, dict[str, object]],
) -> str:
    """navigation tree を HTML に変換する。"""

    rendered_items: list[str] = []

    for item in items:
        title = html.escape(str(item.get("title", "")))
        doc_id = item.get("doc_id")
        children = item.get("children", [])

        if doc_id and doc_id in pages_by_doc_id:
            page = pages_by_doc_id[str(doc_id)]
            path = html.escape(str(page["output_html_path"]))
            label = f'<a href="{path}">{title}</a>'
        else:
            label = title

        child_html = ""

        if isinstance(children, list) and children:
            child_html = f"<ul>{render_navigation_items(children, pages_by_doc_id)}</ul>"

        rendered_items.append(f"<li>{label}{child_html}</li>")

    return "".join(rendered_items)


def render_document_map(
    pages: list[dict[str, object]],
    not_generated_documents: list[dict[str, object]],
) -> str:
    """Document Map を HTML table として生成する。"""

    rows: list[str] = []

    for page in pages:
        if "reference" not in page.get("profile", []):
            continue

        title = html.escape(str(page.get("canonical_title", "")))
        doc_id = html.escape(str(page.get("doc_id", "")))
        source = html.escape(str(page.get("source_markdown", "")))
        output = html.escape(str(page.get("output_html_path", "")))
        policy = html.escape(str(page.get("presentation_policy", "")))

        rows.append(
            "<tr>"
            f"<td>{title}</td>"
            f"<td>{doc_id}</td>"
            f"<td>{policy}</td>"
            f'<td><a href="{output}">HTML</a></td>'
            f"<td>{source}</td>"
            "</tr>"
        )

    for item in not_generated_documents:
        title = html.escape(str(item.get("canonical_title", "")))
        doc_id = html.escape(str(item.get("doc_id", "")))
        source = html.escape(str(item.get("source_markdown", "")))
        policy = html.escape(str(item.get("presentation_policy", "")))

        rows.append(
            "<tr>"
            f"<td>{title}</td>"
            f"<td>{doc_id}</td>"
            f"<td>{policy}</td>"
            "<td>-</td>"
            f"<td>{source}</td>"
            "</tr>"
        )

    return (
        "<table>"
        "<thead><tr>"
        "<th>Title</th><th>doc_id</th><th>policy</th><th>HTML</th><th>Markdown</th>"
        "</tr></thead>"
        f"<tbody>{''.join(rows)}</tbody>"
        "</table>"
    )


def write_index_page(
    output_root: Path,
    pages: list[dict[str, object]],
    generated_at: str,
    not_generated_documents: list[dict[str, object]],
    navigation_model: dict[str, Any] | None,
) -> None:
    """HTML ドキュメント入口 index.html を生成する。"""

    reference_items: list[str] = []
    navigation_html = ""

    if navigation_model:
        pages_by_doc_id = {
            str(page["doc_id"]): page
            for page in pages
            if page.get("doc_id") and page.get("output_html_path")
        }
        items = navigation_model.get("items", [])

        if isinstance(items, list) and items:
            navigation_html = f"""
  <section>
    <h2>Navigation</h2>
    <ul>{render_navigation_items(items, pages_by_doc_id)}</ul>
  </section>
"""

    for page in pages:
        if "reference" not in page.get("profile", []):
            continue
        title = str(page["canonical_title"])
        path = str(page["output_html_path"])
        policy = str(page.get("presentation_policy", ""))
        reference_items.append(
            f"<li><a href=\"{html.escape(path)}\">{html.escape(title)}</a> [{html.escape(policy)}]</li>"
        )

    not_generated_items = ["<li>traceability</li>", "<li>test-report</li>"]

    for item in not_generated_documents:
        title = html.escape(str(item["canonical_title"]))
        source = html.escape(str(item["source_markdown"]))
        reason = item.get("reason")
        reason_html = f" - {html.escape(str(reason))}" if reason else ""
        not_generated_items.append(f"<li>{title} ({source}){reason_html}</li>")

    document_map_html = f"""
  <section>
    <h2>Document Map</h2>
    {render_document_map(pages, not_generated_documents)}
  </section>
"""

    body_html = f"""
<header>
  <h1>HLDocS HTMLドキュメント</h1>
</header>
<main>
  <section class=\"meta\">
    <p><strong>generated_at:</strong> {html.escape(generated_at)}</p>
    <p><strong>profile:</strong> overview, reference</p>
  </section>
  <section>
    <h2>Overview</h2>
    <p><a href=\"overview/index.html\">HLDocS HTML Overview</a></p>
  </section>
  {navigation_html}
  {document_map_html}
  <section>
    <h2>Reference</h2>
    <ul>{''.join(reference_items)}</ul>
  </section>
  <section>
    <h2>Not generated</h2>
    <ul>{''.join(not_generated_items)}</ul>
  </section>
</main>
"""
    (output_root / "index.html").write_text(
        html_page("HLDocS HTMLドキュメント", body_html),
        encoding="utf-8",
    )
