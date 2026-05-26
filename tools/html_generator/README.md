# HLDocS HTML Generator PoC

## 1. 位置付け

本ディレクトリは、HLDocS 自身を対象とした HTML 生成 PoC の最小実装を格納する。

HTML は Markdown 正本を置き換えるものではなく、read-only Operational Representation として生成する。

本ディレクトリは Generate 系責務のみを扱う。

```text
Canonical Markdown
→ Operational HTML
```

---

## 2. markdown_viewer との責務分離

markdown_viewer は html_generator の runtime subsystem ではない。

markdown_viewer は以下を目的とする。

```text
Canonical Markdown Browser
```

一方、html_generator は以下を扱う。

```text
- HTML generation
- relationship analysis
- operational visualization
- presentation generation
- summarization
```

---

## 3. html_generator の責務

html_generator は Generate 系責務を扱う。

### 対象

```text
- HTML generation
- relationship graph generation
- presentation generation
- operational visualization
- summarization
- transformation
```

### 非対象

```text
- lightweight markdown browsing
- local markdown navigation UI
- source browsing
```

これらは markdown_viewer 側責務。

---

## 4. 対象 profile

初期 PoC では、以下のみを対象とする。

- `overview`
- `reference`

以下は対象外とする。

- `traceability`
- `test-report`

対象外 profile は、HTML 上では `not generated` として扱う。

---

## 5. ディレクトリ構成

```text
tools/
├── html_generator/
│   ├── generate_html.py
│   ├── hldocs_html/
│   │   ├── constants.py
│   │   ├── models.py
│   │   ├── markdown_loader.py
│   │   ├── presentation_model.py
│   │   ├── renderer.py
│   │   ├── manifest.py
│   │   └── generator.py
│   ├── tests/
│   └── test_generate_html.py
└── markdown_viewer/
    ├── viewer.js
    ├── viewer.css
    ├── viewer_template.py
    └── README.md
```

---

## 6. html_generator 側へ残すもの

以下は html_generator 側へ残す。

```text
- relationship model
- operational graph
- generated visualization
- dependency analysis
- presentation model
- summarization visualization
```

---

## 7. html_generator 側へ残さないもの

以下は markdown_viewer 側へ分離する。

```text
- markdown render UI
- TOC UI
- source toggle UI
- hash navigation UI
- sticky toolbar
- Mermaid render UI
```

---

## 8. viewer/runtime 化禁止

html_generator は markdown_viewer を以下へ拡張しない。

```text
- graph runtime
- runtime platform
- projection runtime
- distributed synchronization runtime
```

これらが必要なら別責務として扱う。

---

## 9. 実行方法

リポジトリルートから以下を実行する。

### 9.1 bash / Git Bash

```bash
python tools/html_generator/generate_html.py \
  --input docs/ja-JP \
  --output docs/ja-JP/HTMLドキュメント \
  --profile overview,reference
```

### 9.2 PowerShell

PowerShell では、改行継続に `^` ではなくバッククォート `` ` `` を使用する。

```powershell
python tools/html_generator/generate_html.py `
  --input docs/ja-JP `
  --output docs/ja-JP/HTMLドキュメント `
  --profile overview,reference
```

### 9.3 cmd.exe

```cmd
python tools/html_generator/generate_html.py ^
  --input docs/ja-JP ^
  --output docs/ja-JP/HTMLドキュメント ^
  --profile overview,reference
```

---

## 10. Presentation Model

Presentation Model は以下に配置する。

```text
docs/ja-JP/HTMLドキュメント/Presentation-Model/
```

対応 policy は以下とする。

| policy | 意味 |
| --- | --- |
| `full_render` | Markdown 本文を簡易 HTML 化する。 |
| `overview_only` | 概要と見出しのみ表示する。 |
| `link_only` | Markdown 正本リンクのみを主導線にする。 |
| `not_generated` | reference HTML を生成せず、Not generated / Document Map に表示する。 |

---

## 11. 生成物

以下が生成される。

```text
docs/ja-JP/HTMLドキュメント/
├── overview/
├── reference/
├── manifest/
└── index.html
```

---

## 12. テスト実行

```bash
python -m pytest tools/html_generator/tests
```

---

## 13. 注意点

- 本実装は PoC 用であり、正式 generator ではない。
- Markdown 変換は最小実装である。
- `sec_id` は推測生成しない。
- Manifest に存在しない内部リンクは生成しない。
- generated artifact のファイル名・ディレクトリ名には空白を含めない。

---

## 14. アーキテクチャ原則

### html_generator

```text
Generate Layer
```

### markdown_viewer

```text
Browse Layer
```

### Runtime

```text
別責務
```

Browse / Generate / Runtime を混在させない。
