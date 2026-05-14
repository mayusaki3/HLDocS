# HLDocS HTML Generator PoC

## 1. 位置付け

本ディレクトリは、HLDocS 自身を対象とした HTML 生成 PoC の最小実装を格納する。

HTML は Markdown 正本を置き換えるものではなく、read-only Operational Representation として生成する。

---

## 2. 対象 profile

初期 PoC では、以下のみを対象とする。

- `overview`
- `reference`

以下は対象外とする。

- `traceability`
- `test-report`

対象外 profile は、HTML 上では `not generated` として扱う。

---

## 3. ディレクトリ構成

```text
tools/html_generator/
├── generate_html.py
├── hldocs_html/
│   ├── constants.py
│   ├── models.py
│   ├── markdown_loader.py
│   ├── presentation_model.py
│   ├── renderer.py
│   ├── manifest.py
│   └── generator.py
├── tests/
│   ├── test_markdown_loader.py
│   ├── test_presentation_model.py
│   ├── test_renderer.py
│   └── test_generator.py
└── test_generate_html.py
```

役割は以下とする。

| Path | 役割 |
| --- | --- |
| `generate_html.py` | CLI 互換入口。実処理は `hldocs_html` へ委譲する。 |
| `hldocs_html/markdown_loader.py` | Markdown 正本列挙、LLM-MANAGED metadata 抽出、見出し・sec_id 抽出。 |
| `hldocs_html/presentation_model.py` | Presentation Model 読み込み、presentation_policy 解決、navigation 読み込み。 |
| `hldocs_html/renderer.py` | reference / overview / index / Navigation / Document Map の HTML 生成。 |
| `hldocs_html/manifest.py` | HTML Site Manifest 生成、生成パス検査。 |
| `hldocs_html/generator.py` | 全体 orchestration。 |
| `tests/` | 責務別テスト。CI の実行対象。 |
| `test_generate_html.py` | 旧ローカルコマンド互換用テスト入口。 |

---

## 4. 実行方法

リポジトリルートから以下を実行する。

### 4.1 bash / Git Bash

```bash
python tools/html_generator/generate_html.py \
  --input docs/ja-JP \
  --output docs/ja-JP/HTMLドキュメント \
  --profile overview,reference
```

### 4.2 PowerShell

PowerShell では、改行継続に `^` ではなくバッククォート `` ` `` を使用する。

```powershell
python tools/html_generator/generate_html.py `
  --input docs/ja-JP `
  --output docs/ja-JP/HTMLドキュメント `
  --profile overview,reference
```

1行で実行してもよい。

```powershell
python tools/html_generator/generate_html.py --input docs/ja-JP --output docs/ja-JP/HTMLドキュメント --profile overview,reference
```

### 4.3 cmd.exe

cmd.exe では、改行継続に `^` を使用する。

```cmd
python tools/html_generator/generate_html.py ^
  --input docs/ja-JP ^
  --output docs/ja-JP/HTMLドキュメント ^
  --profile overview,reference
```

---

## 5. Presentation Model

Presentation Model は以下に配置する。

```text
docs/ja-JP/HTMLドキュメント/Presentation-Model/
```

文書単位 policy は以下に配置する。

```text
docs/ja-JP/HTMLドキュメント/Presentation-Model/documents/*.json
```

site navigation は以下に配置する。

```text
docs/ja-JP/HTMLドキュメント/Presentation-Model/site/navigation.json
```

対応 policy は以下とする。

| policy | 意味 |
| --- | --- |
| `full_render` | Markdown 本文を簡易 HTML 化する。 |
| `overview_only` | 概要と見出しのみ表示する。 |
| `link_only` | Markdown 正本リンクのみを主導線にする。 |
| `not_generated` | reference HTML を生成せず、Not generated / Document Map に表示する。 |

---

## 6. 生成物

以下が生成される。

```text
docs/ja-JP/HTMLドキュメント/
├── overview/
│   └── index.html
├── reference/
│   └── *.html
├── manifest/
│   └── site-manifest.json
└── index.html
```

`index.html` には、現時点で以下を出力する。

- Overview 導線
- Navigation
- Document Map
- Reference 一覧
- Not generated 一覧

---

## 7. テスト実行

CI と同じ責務別テストのみを実行する場合は以下を使用する。

```bash
python -m pytest tools/html_generator/tests
```

旧ローカルコマンド互換入口を確認する場合は以下を使用する。

```bash
python -m pytest tools/html_generator/test_generate_html.py
```

以下は互換入口と責務別テストを両方検出するため、テスト件数が重複する。

```bash
python -m pytest tools/html_generator
```

---

## 8. 注意点

- 本実装は PoC 用であり、正式 generator ではない。
- Markdown 変換は最小実装であり、完全な Markdown 変換器ではない。
- `sec_id` は本文に存在する場合のみ抽出し、推測生成しない。
- Manifest に存在しないページへの内部リンクは生成しない。
- HTML generated artifact のファイル名・ディレクトリ名には空白を含めない。
- `test_generate_html.py` は互換入口であり、新規テストは `tests/` 配下へ追加する。

---

## 9. 後続

PoC の検証結果は、まず `docs/ja-JP/フィードバック` に記録する。

PoC 完了後、必要な内容を HTML 系仕様へ一括反映する。
