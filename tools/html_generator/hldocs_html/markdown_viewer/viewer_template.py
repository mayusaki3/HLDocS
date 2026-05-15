"""Markdown viewer HTML template."""

from __future__ import annotations

VIEWER_HTML = """<!doctype html>
<html lang=\"en\">
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
      <button type=\"button\" id=\"render-mode\" data-i18n=\"render\">Render</button>
      <button type=\"button\" id=\"source-mode\" data-i18n=\"source\">Source</button>
      <button type=\"button\" id=\"top-button\" data-i18n=\"top\">Top</button>
      <button type=\"button\" id=\"previous-section-button\" data-i18n=\"previous\">Previous section</button>
      <button type=\"button\" id=\"next-section-button\" data-i18n=\"next\">Next section</button>
      <button type=\"button\" id=\"bottom-button\" data-i18n=\"bottom\">Bottom</button>
    </nav>
  </header>
  <main>
    <section id=\"metadata\" class=\"metadata-panel\" hidden></section>
    <article id=\"rendered\" class=\"markdown-body\"></article>
    <pre id=\"source\" class=\"markdown-source\" hidden><code></code></pre>
  </main>
  <script src=\"viewer.js\"></script>
</body>
</html>
"""
