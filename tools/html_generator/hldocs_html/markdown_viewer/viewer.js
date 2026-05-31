const metadata = document.getElementById('metadata');
const rendered = document.getElementById('rendered');
const source = document.getElementById('source');
const sourceCode = source.querySelector('code');
const title = document.getElementById('viewer-title');
const renderMode = document.getElementById('render-mode');
const sourceMode = document.getElementById('source-mode');
const topButton = document.getElementById('top-button');
const previousSectionButton = document.getElementById('previous-section-button');
const nextSectionButton = document.getElementById('next-section-button');
const bottomButton = document.getElementById('bottom-button');

const params = new URLSearchParams(window.location.search);
const src = params.get('src');

const translations = {
  'en-US': {
    render: 'Render',
    source: 'Source',
    top: 'Top',
    previous: 'Previous section',
    next: 'Next section',
    bottom: 'Bottom',
    metadata: 'HLDocS Metadata',
    missingSrc: 'src query parameter is required.',
    failedLoad: 'Failed to load Markdown:',
  },
  'ja-JP': {
    render: '表示',
    source: '原文',
    top: '先頭',
    previous: '前の大項目',
    next: '次の大項目',
    bottom: '最後',
    metadata: 'HLDocS Metadata',
    missingSrc: 'src query parameter is required.',
    failedLoad: 'Markdown の読み込みに失敗しました:',
  },
};

let activeLanguage = 'en-US';
let sectionTargets = [];

function detectLanguage(path) {
  const match = path.match(/(?:^|\/)docs\/([a-z]{2}-[A-Z]{2})(?:\/|$)/);

  if (match && translations[match[1]]) {
    return match[1];
  }

  const relativeMatch = path.match(/(?:^|\/)([a-z]{2}-[A-Z]{2})(?:\/|$)/);

  if (relativeMatch && translations[relativeMatch[1]]) {
    return relativeMatch[1];
  }

  return 'en-US';
}

function t(key) {
  return translations[activeLanguage][key] || translations['en-US'][key] || key;
}

function applyI18n() {
  document.documentElement.lang = activeLanguage;

  for (const element of document.querySelectorAll('[data-i18n]')) {
    element.textContent = t(element.dataset.i18n);
  }
}

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

function displayFileName(path) {
  const lastPart = path.split('/').pop() || 'Markdown Viewer';

  try {
    return decodeURIComponent(lastPart);
  } catch (_error) {
    return lastPart;
  }
}

function extractLeadingHtmlComment(markdown) {
  const match = markdown.match(/^\s*<!--([\s\S]*?)-->\s*/);

  if (!match) {
    return { body: markdown, metadata: {} };
  }

  const comment = match[1];
  const body = markdown.slice(match[0].length);
  const parsed = {};

  for (const line of comment.split(/\r?\n/)) {
    const trimmed = line.trim();

    if (!trimmed || trimmed === 'HLDocS:LLM-MANAGED') {
      continue;
    }

    const separatorIndex = trimmed.indexOf(':');

    if (separatorIndex === -1) {
      continue;
    }

    const key = trimmed.slice(0, separatorIndex).trim();
    const value = trimmed.slice(separatorIndex + 1).trim();

    if (key) {
      parsed[key] = value;
    }
  }

  return { body, metadata: parsed };
}

function extractSecIds(markdown) {
  const secIds = new Set();
  const regex = /\bsec_(?!id\b)[A-Za-z0-9][A-Za-z0-9_-]*\b/g;
  let match;

  while ((match = regex.exec(markdown)) !== null) {
    secIds.add(match[0]);
  }

  return [...secIds].sort();
}

function renderMetadataPanel(parsedMetadata, secIds) {
  const rows = [];
  const orderedKeys = [
    'doc_id',
    'canonical_title',
    'document_type',
    'lang',
    'canonical_document',
  ];

  for (const key of orderedKeys) {
    if (parsedMetadata[key] !== undefined) {
      rows.push(`<tr><th>${escapeHtml(key)}</th><td>${escapeHtml(parsedMetadata[key])}</td></tr>`);
    }
  }

  if (secIds.length > 0) {
    rows.push(`<tr><th>sec_id</th><td>${escapeHtml(secIds.join(', '))}</td></tr>`);
  }

  if (rows.length === 0) {
    metadata.hidden = true;
    metadata.dataset.hasMetadata = 'false';
    metadata.innerHTML = '';
    return;
  }

  metadata.hidden = false;
  metadata.dataset.hasMetadata = 'true';
  metadata.innerHTML = `<h2>${escapeHtml(t('metadata'))}</h2><table>${rows.join('')}</table>`;
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
      const sectionClass = level <= 2 ? ' class="major-section"' : '';
      html.push(`<h${level} id="${id}"${sectionClass}>${renderInline(text)}</h${level}>`);
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

function refreshSectionTargets() {
  sectionTargets = [...document.querySelectorAll('.major-section')];
}

function currentSectionIndex() {
  const currentY = window.scrollY + 8;
  let index = -1;

  for (let i = 0; i < sectionTargets.length; i += 1) {
    if (sectionTargets[i].offsetTop <= currentY) {
      index = i;
    }
  }

  return index;
}

function scrollToElement(element) {
  element.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function showRender() {
  metadata.hidden = metadata.dataset.hasMetadata !== 'true';
  rendered.hidden = false;
  source.hidden = true;
}

function showSource() {
  metadata.hidden = true;
  rendered.hidden = true;
  source.hidden = false;
}

renderMode.addEventListener('click', showRender);
sourceMode.addEventListener('click', showSource);
topButton.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
bottomButton.addEventListener('click', () => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }));
previousSectionButton.addEventListener('click', () => {
  const index = currentSectionIndex();
  const target = sectionTargets[Math.max(0, index - 1)];

  if (target) {
    scrollToElement(target);
  }
});
nextSectionButton.addEventListener('click', () => {
  const index = currentSectionIndex();
  const target = sectionTargets[Math.min(sectionTargets.length - 1, index + 1)];

  if (target) {
    scrollToElement(target);
  }
});

async function main() {
  if (!src) {
    rendered.innerHTML = `<div class="error">${escapeHtml(t('missingSrc'))}</div>`;
    return;
  }

  activeLanguage = detectLanguage(src);
  applyI18n();

  const response = await fetch(src);

  if (!response.ok) {
    rendered.innerHTML = `<div class="error">${escapeHtml(t('failedLoad'))} ${escapeHtml(src)}</div>`;
    return;
  }

  const markdown = await response.text();
  const parsed = extractLeadingHtmlComment(markdown);
  const secIds = extractSecIds(parsed.body);
  const decodedTitle = displayFileName(src);

  title.textContent = decodedTitle;
  document.title = decodedTitle;
  sourceCode.textContent = markdown;
  renderMetadataPanel(parsed.metadata, secIds);
  rendered.innerHTML = renderMarkdown(parsed.body);
  refreshSectionTargets();

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
