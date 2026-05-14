"""Markdown viewer asset generation.

役割:
    HTML generated artifact として Markdown viewer 一式を生成する。

注意点:
    - Markdown 正本を変更しない。
    - viewer は static HTML / CSS / JavaScript のみで動作する。
    - PoC 用の最小 renderer であり、GitHub Markdown viewer 完全互換ではない。
"""

from __future__ import annotations

from pathlib import Path


VIEWER_HTML = """<!doctype html>
<html lang=\"ja\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>Markdown Viewer</title>
  <link rel=\"stylesheet\" href=\"viewer.css\">
</head>
<body>
  <header class=\"viewer-header\">
    <h1 id=\"viewer-title\">Markdown Viewer</h1>
    <nav class=\"viewer-toolbar\">
      <button type=\"button\" id=\"render-mode\">Render</button>
      <button type=\"button\" id=\"source-mode\">Source</button>
      <a id=\"raw-link\" href=\"#\" target=\"_blank\" rel=\"noopener noreferrer\">Raw Markdown</a>
    </nav>
  </header>
  <main>
    <article id=\"rendered\" class=\"markdown-body\"></article>
    <pre id=\"source\" class=\"markdown-source\" hidden><code></code></pre>
  </main>
  <script src=\"viewer.js\"></script>
</body>
</html>
"""


VIEWER_CSS = """body {
  font-family: sans-serif;
  line-height: 1.7;
  margin: 2rem;
  max-width: 1080px;
}

.viewer-header {
  border-bottom: 1px solid #ddd;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
}

.viewer-toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.viewer-toolbar button,
.viewer-toolbar a {
  border: 1px solid #ccc;
  border-radius: 0.25rem;
  background: #f8f8f8;
  color: #222;
  cursor: pointer;
  padding: 0.35rem 0.7rem;
  text-decoration: none;
}

.markdown-body h1,
.markdown-body h2,
.markdown-body h3 {
  border-bottom: 1px solid #eee;
  padding-bottom: 0.2rem;
}

.markdown-body pre,
.markdown-source {
  background: #f5f5f5;
  overflow-x: auto;
  padding: 1rem;
}

.markdown-body code {
  background: #f5f5f5;
  padding: 0.1rem 0.25rem;
}

.markdown-body table {
  border-collapse: collapse;
  width: 100%;
}

.markdown-body th,
.markdown-body td {
  border: 1px solid #ddd;
  padding: 0.5rem;
  text-align: left;
  vertical-align: top;
}

.markdown-body blockquote {
  border-left: 4px solid #ddd;
  color: #555;
  margin-left: 0;
  padding-left: 1rem;
}

.error {
  border: 1px solid #d99;
  background: #fff7f7;
  padding: 1rem;
}
"""


VIEWER_JS = r"""const rendered = document.getElementById('rendered');
const source = document.getElementById('source');
const sourceCode = source.querySelector('code');
const title = document.getElementById('viewer-title');
const rawLink = document.getElementById('raw-link');
const renderMode = document.getElementById('render-mode');
const sourceMode = document.getElementById('source-mode');

const params = new URLSearchParams(window.location.search);
const src = params.get('src');

function escapeHtml(value) {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function slugify(value) {
  return value
    .trim()
    .toLowerCase()
    .replace(/[\s]+/g, '-')
    .replace(/[^0-9a-z\u3040-\u30ff\u3400-\u9fff_-]/g, '-');
}

function resolveMarkdownLink(href) {
  if (!src || href.startsWith('#') || href.match(/^[a-zA-Z][a-zA-Z0-9+.-]*:/)) {
    return href;
  }

  const [pathPart, hashPart] = href.split('#');

  if (!pathPart.endsWith('.md')) {
    return href;
  }

  const resolved = new URL(pathPart, new URL(src, window.location.href)).href;
  const relative = new URL(resolved).pathname;
  const viewerUrl = new URL(window.location.href);
  viewerUrl.search = `?src=${encodeURIComponent(relative)}`;
  viewerUrl.hash = hashPart ? slugify(decodeURIComponent(hashPart)) : '';
  return viewerUrl.pathname + viewerUrl.search + viewerUrl.hash;
}

function renderInline(value) {
  let escaped = escapeHtml(value);

  escaped = escaped.replace(/`([^`]+)`/g, '<code>$1</code>');
  escaped = escaped.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_match, label, href) => {
    return `<a href="${escapeHtml(resolveMarkdownLink(href))}">${escapeHtml(label)}</a>`;
  });

  return escaped;
}

function renderMarkdown(markdown) {
  const lines = markdown.split(/\r?\n/);
  const html = [];
  let inCode = false;
  let codeLines = [];
  let inList = false;

  function closeList() {
    if (inList) {
      html.push('</ul>');
      inList = false;
    }
  }

  for (const line of lines) {
    if (line.startsWith('```')) {
      if (inCode) {
        html.push(`<pre><code>${escapeHtml(codeLines.join('\n'))}</code></pre>`);
        codeLines = [];
        inCode = false;
      } else {
        closeList();
        inCode = true;
      }
      continue;
    }

    if (inCode) {
      codeLines.push(line);
      continue;
    }

    const heading = line.match(/^(#{1,6})\s+(.+?)\s*$/);
    if (heading) {
      closeList();
      const level = heading[1].length;
      const text = heading[2];
      const id = slugify(text);
      html.push(`<h${level} id="${id}">${renderInline(text)}</h${level}>`);
      continue;
    }

    const listItem = line.match(/^[-*]\s+(.+?)\s*$/);
    if (listItem) {
      if (!inList) {
        html.push('<ul>');
        inList = true;
      }
      html.push(`<li>${renderInline(listItem[1])}</li>`);
      continue;
    }

    if (!line.trim()) {
      closeList();
      continue;
    }

    closeList();
    html.push(`<p>${renderInline(line)}</p>`);
  }

  closeList();

  if (inCode) {
    html.push(`<pre><code>${escapeHtml(codeLines.join('\n'))}</code></pre>`);
  }

  return html.join('\n');
}

function showRender() {
  rendered.hidden = false;
  source.hidden = true;
}

function showSource() {
  rendered.hidden = true;
  source.hidden = false;
}

renderMode.addEventListener('click', showRender);
sourceMode.addEventListener('click', showSource);

async function main() {
  if (!src) {
    rendered.innerHTML = '<div class="error">src query parameter is required.</div>';
    return;
  }

  rawLink.href = src;

  const response = await fetch(src);

  if (!response.ok) {
    rendered.innerHTML = `<div class="error">Failed to load Markdown: ${escapeHtml(src)}</div>`;
    return;
  }

  const markdown = await response.text();
  title.textContent = src.split('/').pop() || 'Markdown Viewer';
  document.title = title.textContent;
  sourceCode.textContent = markdown;
  rendered.innerHTML = renderMarkdown(markdown);

  if (window.location.hash) {
    const target = document.getElementById(decodeURIComponent(window.location.hash.slice(1)));
    if (target) {
      target.scrollIntoView();
    }
  }
}

main().catch((error) => {
  rendered.innerHTML = `<div class="error">${escapeHtml(String(error))}</div>`;
});
"""


def markdown_viewer_link(markdown_source_path: str) -> str:
    """reference ページから Markdown viewer への相対リンクを生成する。"""

    return f"../markdown/viewer.html?src={markdown_source_path}"


def write_markdown_viewer_assets(output_root: Path) -> None:
    """Markdown viewer assets を生成する。"""

    viewer_dir = output_root / "markdown"
    viewer_dir.mkdir(parents=True, exist_ok=True)

    (viewer_dir / "viewer.html").write_text(VIEWER_HTML, encoding="utf-8")
    (viewer_dir / "viewer.css").write_text(VIEWER_CSS, encoding="utf-8")
    (viewer_dir / "viewer.js").write_text(VIEWER_JS, encoding="utf-8")
