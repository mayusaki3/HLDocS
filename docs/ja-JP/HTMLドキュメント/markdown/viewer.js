const rendered = document.getElementById('rendered');
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
